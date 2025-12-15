# Horloq 技術設計書

## システム概要

HorloqはPython 3.11+とCustomTkinterを使用したデスクトップアプリケーションです。シングルプロセスで動作し、プラグインシステムにより、ユーザーが機能を拡張できる柔軟な設計を採用しています。

## 技術詳細設計

### 1. アプリケーションエントリーポイント

#### 1.1 メインアプリケーション

```python
# horloq/__main__.py
import sys
from horloq.core.app import HorloqApp
from horloq.utils.logger import setup_logger

def main():
    """アプリケーションのエントリーポイント"""
    # ロガーの初期化
    logger = setup_logger()
    logger.info("Horloq starting...")
    
    try:
        # アプリケーションの作成と実行
        app = HorloqApp()
        app.run()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)
    
    logger.info("Horloq terminated")

if __name__ == "__main__":
    main()
```

#### 1.2 メインアプリケーションクラス

```python
# horloq/core/app.py
import customtkinter as ctk
from pathlib import Path
from typing import Optional

from horloq.core.config import ConfigManager
from horloq.core.window import MainWindow
from horloq.core.events import EventSystem
from horloq.core.theme import ThemeManager
from horloq.plugins.manager import PluginManager
from horloq.utils.logger import get_logger

class HorloqApp:
    """Horloqメインアプリケーション"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # 設定ディレクトリの作成
        self.config_dir = Path.home() / ".horloq"
        self.config_dir.mkdir(exist_ok=True)
        
        # コアコンポーネントの初期化
        self.config = ConfigManager(self.config_dir / "config.yaml")
        self.events = EventSystem()
        self.theme = ThemeManager(self.config, self.events)
        
        # プラグインシステムの初期化
        self.plugin_manager = PluginManager(
            plugin_dir=Path(__file__).parent.parent.parent / "plugins",
            config=self.config,
            events=self.events
        )
        
        # メインウィンドウ
        self.window: Optional[MainWindow] = None
    
    def run(self):
        """アプリケーションの実行"""
        try:
            # テーマの適用
            self.theme.apply()
            
            # メインウィンドウの作成
            self.window = MainWindow(
                config=self.config,
                events=self.events,
                theme=self.theme,
                plugin_manager=self.plugin_manager
            )
            
            # プラグインのロード
            self.plugin_manager.load_all()
            
            # 有効なプラグインのアクティベート
            enabled_plugins = self.config.get("plugins.enabled", [])
            for plugin_id in enabled_plugins:
                try:
                    self.plugin_manager.enable_plugin(plugin_id)
                except Exception as e:
                    self.logger.error(f"Failed to enable plugin {plugin_id}: {e}")
            
            # メインループの開始
            self.window.mainloop()
            
        except Exception as e:
            self.logger.error(f"Failed to run application: {e}", exc_info=True)
            raise
        finally:
            # クリーンアップ
            self.cleanup()
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        self.logger.info("Cleaning up...")
        
        # すべてのプラグインを無効化
        for plugin_id in self.plugin_manager.get_enabled_plugins():
            try:
                self.plugin_manager.disable_plugin(plugin_id)
            except Exception as e:
                self.logger.error(f"Error disabling plugin {plugin_id}: {e}")
        
        # 設定の保存
        try:
            self.config.save()
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
```

### 2. 設定管理システム

#### 2.1 設定ストレージ

```typescript
// main/config.ts
import Store from 'electron-store';

interface AppConfig {
  // ウィンドウ設定
  window: {
    width: number;
    height: number;
    x?: number;
    y?: number;
    alwaysOnTop: boolean;
    transparent: boolean;
    opacity: number;
  };
  
  // 時計設定
  clock: {
    format: '12h' | '24h';
    showSeconds: boolean;
    showDate: boolean;
    dateFormat: string;
    timezone: string;
  };
  
  // テーマ設定
  theme: {
    name: string;
    colors: {
      background: string;
      text: string;
      accent: string;
    };
    font: {
      family: string;
      size: number;
      weight: string;
    };
  };
  
  // プラグイン設定
  plugins: {
    enabled: string[];
    configs: Record<string, any>;
  };
  
  // 一般設定
  general: {
    language: string;
    autoStart: boolean;
    checkUpdates: boolean;
  };
}

export class ConfigManager {
  private static store: Store<AppConfig>;
  
  static initialize() {
    this.store = new Store<AppConfig>({
      defaults: this.getDefaults(),
      name: 'config',
      encryptionKey: 'horloq-secret-key', // 本番環境では適切に管理
    });
  }
  
  static getDefaults(): AppConfig {
    return {
      window: {
        width: 400,
        height: 200,
        alwaysOnTop: true,
        transparent: false,
        opacity: 1.0,
      },
      clock: {
        format: '24h',
        showSeconds: true,
        showDate: true,
        dateFormat: 'YYYY/MM/DD',
        timezone: 'Asia/Tokyo',
      },
      theme: {
        name: 'default',
        colors: {
          background: '#1a1a1a',
          text: '#ffffff',
          accent: '#00a8ff',
        },
        font: {
          family: 'Roboto, sans-serif',
          size: 48,
          weight: 'normal',
        },
      },
      plugins: {
        enabled: [],
        configs: {},
      },
      general: {
        language: 'ja',
        autoStart: false,
        checkUpdates: true,
      },
    };
  }
  
  static get<K extends keyof AppConfig>(key: K): AppConfig[K] {
    return this.store.get(key);
  }
  
  static set<K extends keyof AppConfig>(key: K, value: AppConfig[K]): void {
    this.store.set(key, value);
  }
  
  static reset(): void {
    this.store.clear();
    this.store.set(this.getDefaults());
  }
}
```

### 3. プラグインシステム

#### 3.1 プラグインインターフェース

```typescript
// shared/types/plugin.ts
export interface PluginManifest {
  id: string;
  name: string;
  version: string;
  description: string;
  author: string;
  homepage?: string;
  main: string;
  permissions: Permission[];
  dependencies?: Record<string, string>;
}

export enum Permission {
  NETWORK = 'network',
  FILE_SYSTEM = 'file_system',
  NOTIFICATIONS = 'notifications',
  SYSTEM_INFO = 'system_info',
  LOCATION = 'location',
}

export interface Plugin {
  manifest: PluginManifest;
  activate(api: PluginAPI): Promise<void>;
  deactivate(): Promise<void>;
}

export interface PluginAPI {
  ui: UIApi;
  storage: StorageApi;
  http: HttpApi;
  system: SystemApi;
  events: EventApi;
}
```

#### 3.2 プラグインマネージャー

```typescript
// main/plugins/manager.ts
import * as path from 'path';
import * as fs from 'fs/promises';
import { Plugin, PluginManifest } from '../../shared/types/plugin';

export class PluginManager {
  private plugins: Map<string, Plugin> = new Map();
  private pluginDir: string;
  
  constructor(pluginDir: string) {
    this.pluginDir = pluginDir;
  }
  
  async loadAll(): Promise<void> {
    const pluginDirs = await fs.readdir(this.pluginDir);
    
    for (const dir of pluginDirs) {
      try {
        await this.loadPlugin(dir);
      } catch (error) {
        console.error(`Failed to load plugin ${dir}:`, error);
      }
    }
  }
  
  async loadPlugin(pluginId: string): Promise<void> {
    const pluginPath = path.join(this.pluginDir, pluginId);
    const manifestPath = path.join(pluginPath, 'manifest.json');
    
    // マニフェストの読み込み
    const manifestData = await fs.readFile(manifestPath, 'utf-8');
    const manifest: PluginManifest = JSON.parse(manifestData);
    
    // プラグインのバリデーション
    this.validateManifest(manifest);
    
    // プラグインのロード
    const mainPath = path.join(pluginPath, manifest.main);
    const plugin: Plugin = require(mainPath).default;
    plugin.manifest = manifest;
    
    this.plugins.set(pluginId, plugin);
  }
  
  async enablePlugin(pluginId: string): Promise<void> {
    const plugin = this.plugins.get(pluginId);
    if (!plugin) {
      throw new Error(`Plugin ${pluginId} not found`);
    }
    
    // プラグインAPIの作成
    const api = this.createPluginAPI(plugin);
    
    // プラグインのアクティベート
    await plugin.activate(api);
    
    // 有効なプラグインリストに追加
    const enabledPlugins = ConfigManager.get('plugins').enabled;
    if (!enabledPlugins.includes(pluginId)) {
      ConfigManager.set('plugins', {
        ...ConfigManager.get('plugins'),
        enabled: [...enabledPlugins, pluginId],
      });
    }
  }
  
  async disablePlugin(pluginId: string): Promise<void> {
    const plugin = this.plugins.get(pluginId);
    if (!plugin) {
      throw new Error(`Plugin ${pluginId} not found`);
    }
    
    // プラグインのディアクティベート
    await plugin.deactivate();
    
    // 有効なプラグインリストから削除
    const enabledPlugins = ConfigManager.get('plugins').enabled;
    ConfigManager.set('plugins', {
      ...ConfigManager.get('plugins'),
      enabled: enabledPlugins.filter(id => id !== pluginId),
    });
  }
  
  private validateManifest(manifest: PluginManifest): void {
    const required = ['id', 'name', 'version', 'main', 'permissions'];
    for (const field of required) {
      if (!manifest[field]) {
        throw new Error(`Manifest missing required field: ${field}`);
      }
    }
  }
  
  private createPluginAPI(plugin: Plugin): PluginAPI {
    return {
      ui: new UIApi(plugin),
      storage: new StorageApi(plugin),
      http: new HttpApi(plugin),
      system: new SystemApi(plugin),
      events: new EventApi(plugin),
    };
  }
}
```

#### 3.3 プラグインAPI実装

```typescript
// main/plugins/api.ts
import { Plugin, Permission } from '../../shared/types/plugin';
import axios from 'axios';

export class UIApi {
  constructor(private plugin: Plugin) {}
  
  showNotification(title: string, message: string): void {
    if (!this.hasPermission(Permission.NOTIFICATIONS)) {
      throw new Error('Plugin does not have notification permission');
    }
    
    // 通知の表示処理
    // ...
  }
  
  addWidget(component: any): void {
    // ウィジェットの追加処理
    // ...
  }
  
  private hasPermission(permission: Permission): boolean {
    return this.plugin.manifest.permissions.includes(permission);
  }
}

export class StorageApi {
  constructor(private plugin: Plugin) {}
  
  async get(key: string): Promise<any> {
    const config = ConfigManager.get('plugins').configs;
    return config[this.plugin.manifest.id]?.[key];
  }
  
  async set(key: string, value: any): Promise<void> {
    const pluginsConfig = ConfigManager.get('plugins');
    const pluginConfig = pluginsConfig.configs[this.plugin.manifest.id] || {};
    
    ConfigManager.set('plugins', {
      ...pluginsConfig,
      configs: {
        ...pluginsConfig.configs,
        [this.plugin.manifest.id]: {
          ...pluginConfig,
          [key]: value,
        },
      },
    });
  }
  
  async delete(key: string): Promise<void> {
    const pluginsConfig = ConfigManager.get('plugins');
    const pluginConfig = pluginsConfig.configs[this.plugin.manifest.id];
    
    if (pluginConfig) {
      delete pluginConfig[key];
      ConfigManager.set('plugins', pluginsConfig);
    }
  }
}

export class HttpApi {
  constructor(private plugin: Plugin) {}
  
  async get(url: string): Promise<any> {
    if (!this.hasPermission(Permission.NETWORK)) {
      throw new Error('Plugin does not have network permission');
    }
    
    const response = await axios.get(url);
    return response.data;
  }
  
  async post(url: string, data: any): Promise<any> {
    if (!this.hasPermission(Permission.NETWORK)) {
      throw new Error('Plugin does not have network permission');
    }
    
    const response = await axios.post(url, data);
    return response.data;
  }
  
  private hasPermission(permission: Permission): boolean {
    return this.plugin.manifest.permissions.includes(permission);
  }
}

export class SystemApi {
  constructor(private plugin: Plugin) {}
  
  getTime(): Date {
    return new Date();
  }
  
  async getLocation(): Promise<{ latitude: number; longitude: number }> {
    if (!this.hasPermission(Permission.LOCATION)) {
      throw new Error('Plugin does not have location permission');
    }
    
    // 位置情報の取得処理
    // ...
    return { latitude: 0, longitude: 0 };
  }
  
  private hasPermission(permission: Permission): boolean {
    return this.plugin.manifest.permissions.includes(permission);
  }
}

export class EventApi {
  private listeners: Map<string, Function[]> = new Map();
  
  constructor(private plugin: Plugin) {}
  
  on(event: string, callback: Function): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
  }
  
  off(event: string, callback: Function): void {
    const listeners = this.listeners.get(event);
    if (listeners) {
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }
  
  emit(event: string, data: any): void {
    const listeners = this.listeners.get(event);
    if (listeners) {
      listeners.forEach(callback => callback(data));
    }
  }
}
```

### 4. UI コンポーネント設計

#### 4.1 時計コンポーネント

```typescript
// renderer/components/Clock/Clock.tsx
import React, { useEffect, useState } from 'react';
import { useConfig } from '../../hooks/useConfig';
import styles from './Clock.module.css';

export const Clock: React.FC = () => {
  const [time, setTime] = useState(new Date());
  const config = useConfig('clock');
  
  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date());
    }, config.showSeconds ? 1000 : 60000);
    
    return () => clearInterval(interval);
  }, [config.showSeconds]);
  
  const formatTime = () => {
    const hours = config.format === '12h' 
      ? time.getHours() % 12 || 12 
      : time.getHours();
    const minutes = time.getMinutes().toString().padStart(2, '0');
    const seconds = time.getSeconds().toString().padStart(2, '0');
    
    let timeStr = `${hours.toString().padStart(2, '0')}:${minutes}`;
    if (config.showSeconds) {
      timeStr += `:${seconds}`;
    }
    if (config.format === '12h') {
      timeStr += time.getHours() >= 12 ? ' PM' : ' AM';
    }
    
    return timeStr;
  };
  
  const formatDate = () => {
    return config.dateFormat
      .replace('YYYY', time.getFullYear().toString())
      .replace('MM', (time.getMonth() + 1).toString().padStart(2, '0'))
      .replace('DD', time.getDate().toString().padStart(2, '0'));
  };
  
  return (
    <div className={styles.clock}>
      <div className={styles.time}>{formatTime()}</div>
      {config.showDate && (
        <div className={styles.date}>{formatDate()}</div>
      )}
    </div>
  );
};
```

#### 4.2 カスタムフック

```typescript
// renderer/hooks/useConfig.ts
import { useEffect, useState } from 'react';
import { AppConfig } from '../../shared/types/config';

export function useConfig<K extends keyof AppConfig>(key: K): AppConfig[K] {
  const [value, setValue] = useState<AppConfig[K]>(null);
  
  useEffect(() => {
    // IPCで設定を取得
    window.electronAPI.config.get(key).then(setValue);
    
    // 設定変更の監視
    const unsubscribe = window.electronAPI.config.onChange(key, setValue);
    
    return () => unsubscribe();
  }, [key]);
  
  return value;
}

export function useConfigSetter<K extends keyof AppConfig>(key: K) {
  return (value: AppConfig[K]) => {
    window.electronAPI.config.set(key, value);
  };
}
```

### 5. データベース設計（プラグインデータ用）

```typescript
// main/database/schema.ts
export interface PluginDataSchema {
  plugins: {
    id: string;
    name: string;
    version: string;
    enabled: boolean;
    installedAt: Date;
    updatedAt: Date;
  };
  
  plugin_data: {
    pluginId: string;
    key: string;
    value: any;
    createdAt: Date;
    updatedAt: Date;
  };
  
  settings: {
    key: string;
    value: any;
    updatedAt: Date;
  };
}
```

### 6. エラーハンドリング

```typescript
// shared/errors.ts
export class HorloqError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: any
  ) {
    super(message);
    this.name = 'HorloqError';
  }
}

export class PluginError extends HorloqError {
  constructor(pluginId: string, message: string, details?: any) {
    super(`Plugin ${pluginId}: ${message}`, 'PLUGIN_ERROR', details);
    this.name = 'PluginError';
  }
}

export class ConfigError extends HorloqError {
  constructor(message: string, details?: any) {
    super(message, 'CONFIG_ERROR', details);
    this.name = 'ConfigError';
  }
}
```

### 7. ロギングシステム

```typescript
// main/logger.ts
import winston from 'winston';
import path from 'path';
import { app } from 'electron';

export class Logger {
  private static instance: winston.Logger;
  
  static initialize() {
    this.instance = winston.createLogger({
      level: process.env.NODE_ENV === 'development' ? 'debug' : 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
      ),
      transports: [
        new winston.transports.File({
          filename: path.join(app.getPath('userData'), 'logs', 'error.log'),
          level: 'error',
        }),
        new winston.transports.File({
          filename: path.join(app.getPath('userData'), 'logs', 'combined.log'),
        }),
      ],
    });
    
    if (process.env.NODE_ENV === 'development') {
      this.instance.add(new winston.transports.Console({
        format: winston.format.simple(),
      }));
    }
  }
  
  static info(message: string, meta?: any) {
    this.instance.info(message, meta);
  }
  
  static error(message: string, error?: Error, meta?: any) {
    this.instance.error(message, { error, ...meta });
  }
  
  static warn(message: string, meta?: any) {
    this.instance.warn(message, meta);
  }
  
  static debug(message: string, meta?: any) {
    this.instance.debug(message, meta);
  }
}
```

## パフォーマンス最適化

### 1. レンダリング最適化
- React.memo でコンポーネントのメモ化
- useMemo / useCallback でリレンダリングの削減
- 仮想化リストでプラグイン一覧の表示

### 2. プラグインの遅延ロード
- 必要時にのみプラグインをロード
- 非同期初期化で起動時間を短縮

### 3. メモリ管理
- 未使用プラグインの自動アンロード
- イベントリスナーの適切なクリーンアップ
- WeakMap の活用

## セキュリティ対策

### 1. コンテキスト分離
- contextIsolation: true
- nodeIntegration: false
- Preload スクリプトでの API 公開

### 2. CSP (Content Security Policy)
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'">
```

### 3. プラグインのサンドボックス化
- 制限された API のみ提供
- 権限ベースのアクセス制御
- プラグインコードの検証

## テスト戦略

### 1. ユニットテスト
- Jest によるロジックのテスト
- プラグインAPI のモック

### 2. 統合テスト
- Spectron による E2E テスト
- IPC 通信のテスト

### 3. プラグインテスト
- プラグイン開発者向けのテストユーティリティ
- モックAPI の提供
