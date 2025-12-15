# Horloq Python実装詳細

## 2. 設定管理システム

### 2.1 設定マネージャー

```python
# horloq/core/config.py
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from copy import deepcopy

class ConfigManager:
    """アプリケーション設定管理"""
    
    DEFAULT_CONFIG = {
        "window": {
            "width": 400,
            "height": 200,
            "x": None,
            "y": None,
            "always_on_top": True,
            "transparent": False,
            "opacity": 1.0,
        },
        "clock": {
            "format": "24h",  # "12h" or "24h"
            "show_seconds": True,
            "show_date": True,
            "date_format": "%Y/%m/%d",
            "timezone": "Asia/Tokyo",
            "font_size": 48,
        },
        "theme": {
            "name": "dark",
            "custom_colors": {
                "bg": "#1a1a1a",
                "fg": "#ffffff",
                "accent": "#00a8ff",
            },
        },
        "plugins": {
            "enabled": [],
            "configs": {},
        },
        "general": {
            "language": "ja",
            "auto_start": False,
            "check_updates": True,
        },
    }
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        """設定ファイルを読み込む"""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded_config = yaml.safe_load(f) or {}
            # デフォルト設定にマージ
            self.config = self._merge_config(self.DEFAULT_CONFIG, loaded_config)
        else:
            self.config = deepcopy(self.DEFAULT_CONFIG)
            self.save()
    
    def save(self):
        """設定ファイルに保存"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """設定値を取得（ドット記法対応）"""
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """設定値を設定（ドット記法対応）"""
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def reset(self):
        """設定をデフォルトに戻す"""
        self.config = deepcopy(self.DEFAULT_CONFIG)
        self.save()
    
    @staticmethod
    def _merge_config(default: dict, loaded: dict) -> dict:
        """設定をマージ（デフォルト + ロード済み）"""
        result = deepcopy(default)
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigManager._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
```

## 3. イベントシステム

```python
# horloq/core/events.py
from typing import Callable, Dict, List, Any
from collections import defaultdict

class EventSystem:
    """イベント管理システム（Observer パターン）"""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
    
    def on(self, event: str, callback: Callable):
        """イベントリスナーを登録"""
        if callback not in self._listeners[event]:
            self._listeners[event].append(callback)
    
    def off(self, event: str, callback: Callable):
        """イベントリスナーを解除"""
        if callback in self._listeners[event]:
            self._listeners[event].remove(callback)
    
    def emit(self, event: str, data: Any = None):
        """イベントを発火"""
        for callback in self._listeners[event]:
            try:
                callback(data)
            except Exception as e:
                print(f"Error in event handler for '{event}': {e}")
    
    def clear(self, event: str = None):
        """イベントリスナーをクリア"""
        if event:
            self._listeners[event].clear()
        else:
            self._listeners.clear()
```

## 4. UIコンポーネント

### 4.1 メインウィンドウ

```python
# horloq/core/window.py
import customtkinter as ctk
from typing import Optional

class MainWindow(ctk.CTk):
    """メインウィンドウ"""
    
    def __init__(self, config, events, theme, plugin_manager):
        super().__init__()
        
        self.config = config
        self.events = events
        self.theme = theme
        self.plugin_manager = plugin_manager
        
        # ウィンドウ設定
        self._setup_window()
        
        # UIコンポーネントの作成
        self._create_widgets()
        
        # イベントリスナーの登録
        self._setup_events()
    
    def _setup_window(self):
        """ウィンドウの初期設定"""
        # タイトルとサイズ
        self.title("Horloq")
        
        width = self.config.get("window.width", 400)
        height = self.config.get("window.height", 200)
        self.geometry(f"{width}x{height}")
        
        # 位置
        x = self.config.get("window.x")
        y = self.config.get("window.y")
        if x is not None and y is not None:
            self.geometry(f"+{x}+{y}")
        
        # 常に最前面
        if self.config.get("window.always_on_top", True):
            self.attributes("-topmost", True)
        
        # 透明度
        opacity = self.config.get("window.opacity", 1.0)
        self.attributes("-alpha", opacity)
        
        # ウィンドウを閉じるときのイベント
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """ウィジェットの作成"""
        # メインフレーム
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 時計表示領域
        from horloq.ui.clock import ClockWidget
        self.clock_widget = ClockWidget(
            self.main_frame,
            self.config,
            self.events
        )
        self.clock_widget.pack(fill="both", expand=True)
        
        # プラグインウィジェット領域
        self.plugin_frame = ctk.CTkFrame(self.main_frame)
        self.plugin_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # 右クリックメニュー
        self._create_context_menu()
    
    def _create_context_menu(self):
        """コンテキストメニューの作成"""
        import tkinter as tk
        
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="設定", command=self._show_settings)
        self.context_menu.add_command(label="プラグイン管理", command=self._show_plugin_manager)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="終了", command=self._on_closing)
        
        self.bind("<Button-3>", self._show_context_menu)
    
    def _show_context_menu(self, event):
        """コンテキストメニューの表示"""
        self.context_menu.post(event.x_root, event.y_root)
    
    def _show_settings(self):
        """設定ウィンドウを表示"""
        from horloq.ui.settings import SettingsWindow
        SettingsWindow(self, self.config, self.events)
    
    def _show_plugin_manager(self):
        """プラグイン管理ウィンドウを表示"""
        from horloq.ui.plugin_manager import PluginManagerWindow
        PluginManagerWindow(self, self.plugin_manager)
    
    def _setup_events(self):
        """イベントリスナーの設定"""
        self.events.on("config_changed", self._on_config_changed)
    
    def _on_config_changed(self, data):
        """設定変更時の処理"""
        key = data.get("key")
        
        if key.startswith("window."):
            # ウィンドウ設定の再適用
            self._setup_window()
    
    def _on_closing(self):
        """ウィンドウを閉じる"""
        # 現在の位置とサイズを保存
        geometry = self.geometry().split("+")
        size = geometry[0].split("x")
        
        self.config.set("window.width", int(size[0]))
        self.config.set("window.height", int(size[1]))
        
        if len(geometry) > 1:
            self.config.set("window.x", int(geometry[1]))
            self.config.set("window.y", int(geometry[2]))
        
        self.config.save()
        self.destroy()
```

### 4.2 時計ウィジェット

```python
# horloq/ui/clock.py
import customtkinter as ctk
from datetime import datetime
from typing import Optional

class ClockWidget(ctk.CTkFrame):
    """時計表示ウィジェット"""
    
    def __init__(self, parent, config, events):
        super().__init__(parent)
        
        self.config = config
        self.events = events
        self.update_id: Optional[str] = None
        
        # ラベルの作成
        self.time_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", self.config.get("clock.font_size", 48), "bold")
        )
        self.time_label.pack(pady=10)
        
        self.date_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 16)
        )
        
        if self.config.get("clock.show_date", True):
            self.date_label.pack()
        
        # 初回更新
        self.update_time()
        
        # イベントリスナー
        self.events.on("config_changed", self._on_config_changed)
    
    def update_time(self):
        """時刻を更新"""
        now = datetime.now()
        
        # 時刻フォーマット
        clock_format = self.config.get("clock.format", "24h")
        show_seconds = self.config.get("clock.show_seconds", True)
        
        if clock_format == "12h":
            time_str = now.strftime("%I:%M" + (":%S" if show_seconds else "") + " %p")
        else:
            time_str = now.strftime("%H:%M" + (":%S" if show_seconds else ""))
        
        self.time_label.configure(text=time_str)
        
        # 日付フォーマット
        if self.config.get("clock.show_date", True):
            date_format = self.config.get("clock.date_format", "%Y/%m/%d")
            date_str = now.strftime(date_format)
            self.date_label.configure(text=date_str)
        
        # イベント発火
        self.events.emit("time_update", now)
        
        # 次の更新をスケジュール
        interval = 1000 if show_seconds else 60000
        self.update_id = self.after(interval, self.update_time)
    
    def _on_config_changed(self, data):
        """設定変更時の処理"""
        key = data.get("key")
        
        if key.startswith("clock."):
            # 表示の更新
            if key == "clock.show_date":
                if self.config.get("clock.show_date"):
                    self.date_label.pack()
                else:
                    self.date_label.pack_forget()
            
            elif key == "clock.font_size":
                font_size = self.config.get("clock.font_size", 48)
                self.time_label.configure(font=("Arial", font_size, "bold"))
            
            # 即座に更新
            if self.update_id:
                self.after_cancel(self.update_id)
            self.update_time()
    
    def destroy(self):
        """ウィジェット破棄"""
        if self.update_id:
            self.after_cancel(self.update_id)
        super().destroy()
```

## 5. プラグインシステム実装

### 5.1 プラグインマネージャー

```python
# horloq/plugins/manager.py
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional
import yaml

from horloq.plugins.base import PluginBase
from horloq.plugins.api import PluginAPI
from horloq.utils.logger import get_logger

class PluginManager:
    """プラグイン管理"""
    
    def __init__(self, plugin_dir: Path, config, events):
        self.plugin_dir = plugin_dir
        self.config = config
        self.events = events
        self.logger = get_logger(__name__)
        
        self.plugins: Dict[str, dict] = {}  # plugin_id -> plugin info
        self.active_plugins: Dict[str, PluginBase] = {}  # plugin_id -> instance
    
    def load_all(self):
        """すべてのプラグインを検索・ロード"""
        if not self.plugin_dir.exists():
            self.logger.warning(f"Plugin directory not found: {self.plugin_dir}")
            return
        
        for plugin_path in self.plugin_dir.iterdir():
            if plugin_path.is_dir() and not plugin_path.name.startswith("_"):
                try:
                    self._load_plugin(plugin_path)
                except Exception as e:
                    self.logger.error(f"Failed to load plugin {plugin_path.name}: {e}")
    
    def _load_plugin(self, plugin_path: Path):
        """個別のプラグインをロード"""
        # マニフェスト読み込み
        manifest_path = plugin_path / "manifest.yaml"
        if not manifest_path.exists():
            raise FileNotFoundError(f"manifest.yaml not found in {plugin_path}")
        
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
        
        plugin_id = manifest["id"]
        
        # プラグインモジュールのパスを構築
        main_file = manifest.get("main", "plugin.py")
        plugin_file = plugin_path / main_file
        
        if not plugin_file.exists():
            raise FileNotFoundError(f"Plugin main file not found: {plugin_file}")
        
        # プラグイン情報を保存
        self.plugins[plugin_id] = {
            "manifest": manifest,
            "path": plugin_path,
            "module_path": plugin_file,
        }
        
        self.logger.info(f"Loaded plugin: {plugin_id} v{manifest['version']}")
    
    def enable_plugin(self, plugin_id: str):
        """プラグインを有効化"""
        if plugin_id in self.active_plugins:
            self.logger.warning(f"Plugin {plugin_id} is already active")
            return
        
        if plugin_id not in self.plugins:
            raise ValueError(f"Plugin {plugin_id} not found")
        
        plugin_info = self.plugins[plugin_id]
        
        # モジュールの動的インポート
        spec = importlib.util.spec_from_file_location(
            f"plugins.{plugin_id}",
            plugin_info["module_path"]
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # プラグインクラスの取得
        plugin_class = getattr(module, "Plugin", None)
        if not plugin_class:
            raise AttributeError(f"Plugin class not found in {plugin_id}")
        
        # プラグインAPIの作成
        api = PluginAPI(plugin_id, self.config, self.events)
        
        # プラグインインスタンスの作成
        plugin_instance = plugin_class(api)
        
        # プラグインのアクティベート
        plugin_instance.activate()
        
        # アクティブプラグインに追加
        self.active_plugins[plugin_id] = plugin_instance
        
        # 有効なプラグインリストに追加
        enabled = self.config.get("plugins.enabled", [])
        if plugin_id not in enabled:
            enabled.append(plugin_id)
            self.config.set("plugins.enabled", enabled)
            self.config.save()
        
        self.logger.info(f"Enabled plugin: {plugin_id}")
        self.events.emit("plugin_enabled", {"plugin_id": plugin_id})
    
    def disable_plugin(self, plugin_id: str):
        """プラグインを無効化"""
        if plugin_id not in self.active_plugins:
            self.logger.warning(f"Plugin {plugin_id} is not active")
            return
        
        plugin_instance = self.active_plugins[plugin_id]
        
        # プラグインのディアクティベート
        plugin_instance.deactivate()
        
        # アクティブプラグインから削除
        del self.active_plugins[plugin_id]
        
        # 有効なプラグインリストから削除
        enabled = self.config.get("plugins.enabled", [])
        if plugin_id in enabled:
            enabled.remove(plugin_id)
            self.config.set("plugins.enabled", enabled)
            self.config.save()
        
        self.logger.info(f"Disabled plugin: {plugin_id}")
        self.events.emit("plugin_disabled", {"plugin_id": plugin_id})
    
    def get_all_plugins(self) -> List[dict]:
        """すべてのプラグイン情報を取得"""
        return [
            {
                "id": plugin_id,
                **info["manifest"],
                "enabled": plugin_id in self.active_plugins,
            }
            for plugin_id, info in self.plugins.items()
        ]
    
    def get_enabled_plugins(self) -> List[str]:
        """有効なプラグインIDのリストを取得"""
        return list(self.active_plugins.keys())
```

### 5.2 プラグイン基底クラス

```python
# horloq/plugins/base.py
from abc import ABC, abstractmethod

class PluginBase(ABC):
    """プラグインの基底クラス"""
    
    def __init__(self, api):
        self.api = api
    
    @abstractmethod
    def activate(self):
        """プラグインが有効化されたときに呼ばれる"""
        pass
    
    @abstractmethod
    def deactivate(self):
        """プラグインが無効化されたときに呼ばれる"""
        pass
```

### 5.3 プラグインAPI

```python
# horloq/plugins/api.py
from typing import Any
import requests
from datetime import datetime

class PluginAPI:
    """プラグインが使用できるAPI"""
    
    def __init__(self, plugin_id: str, config, events):
        self.plugin_id = plugin_id
        self._config = config
        self._events = events
        
        self.ui = UIApi(plugin_id, events)
        self.storage = StorageApi(plugin_id, config)
        self.http = HttpApi(plugin_id)
        self.system = SystemApi()
        self.events = EventApi(plugin_id, events)

class UIApi:
    """UI操作API"""
    
    def __init__(self, plugin_id: str, events):
        self.plugin_id = plugin_id
        self._events = events
    
    def show_notification(self, message: str):
        """通知を表示"""
        self._events.emit("notification", {
            "plugin_id": self.plugin_id,
            "message": message
        })
    
    def add_widget(self, widget):
        """ウィジェットを追加"""
        self._events.emit("add_widget", {
            "plugin_id": self.plugin_id,
            "widget": widget
        })
    
    def remove_widget(self, widget):
        """ウィジェットを削除"""
        self._events.emit("remove_widget", {
            "plugin_id": self.plugin_id,
            "widget": widget
        })

class StorageApi:
    """ストレージAPI"""
    
    def __init__(self, plugin_id: str, config):
        self.plugin_id = plugin_id
        self._config = config
    
    def get(self, key: str, default: Any = None) -> Any:
        """データを取得"""
        return self._config.get(f"plugins.configs.{self.plugin_id}.{key}", default)
    
    def set(self, key: str, value: Any):
        """データを保存"""
        self._config.set(f"plugins.configs.{self.plugin_id}.{key}", value)
        self._config.save()
    
    def delete(self, key: str):
        """データを削除"""
        config_path = f"plugins.configs.{self.plugin_id}.{key}"
        # 実装は省略（辞書から削除）

class HttpApi:
    """HTTP通信API"""
    
    def __init__(self, plugin_id: str):
        self.plugin_id = plugin_id
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """GETリクエスト"""
        return requests.get(url, **kwargs)
    
    def post(self, url: str, data: dict, **kwargs) -> requests.Response:
        """POSTリクエスト"""
        return requests.post(url, json=data, **kwargs)

class SystemApi:
    """システム情報API"""
    
    def get_time(self) -> datetime:
        """現在時刻を取得"""
        return datetime.now()
    
    def get_location(self) -> tuple[float, float]:
        """位置情報を取得（権限必要）"""
        # 実装は省略
        raise NotImplementedError("Location API not implemented")

class EventApi:
    """イベントAPI"""
    
    def __init__(self, plugin_id: str, events):
        self.plugin_id = plugin_id
        self._events = events
    
    def on(self, event: str, callback):
        """イベントリスナーを登録"""
        self._events.on(event, callback)
    
    def off(self, event: str, callback):
        """イベントリスナーを解除"""
        self._events.off(event, callback)
    
    def emit(self, event: str, data: Any = None):
        """イベントを発火"""
        self._events.emit(event, data)
```

## 6. PyInstallerビルド設定

```python
# horloq.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['horloq/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('plugins', 'plugins'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Horloq',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUIアプリなのでコンソール非表示
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/horloq.ico',  # アイコンファイル
)
```

## 7. GitHub Actions ワークフロー

```yaml
# .github/workflows/build.yml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        os: [windows-latest, ubuntu-latest, macos-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build with PyInstaller
      run: |
        pyinstaller horloq.spec
    
    - name: Archive artifacts
      uses: actions/upload-artifact@v3
      with:
        name: horloq-${{ matrix.os }}
        path: dist/
    
    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/')
      uses: softprops/action-gh-release@v1
      with:
        files: dist/*
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 8. 依存関係管理

```toml
# pyproject.toml
[tool.poetry]
name = "horloq"
version = "0.1.0"
description = "拡張可能デスクトップ据え置き時計"
authors = ["Your Name <your.email@example.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
customtkinter = "^5.2.0"
Pillow = "^10.0.0"
PyYAML = "^6.0"
requests = "^2.31.0"
python-dateutil = "^2.8.2"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
black = "^23.7.0"
ruff = "^0.0.285"
mypy = "^1.5.0"
pyinstaller = "^5.13.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

```
# requirements.txt
customtkinter>=5.2.0
Pillow>=10.0.0
PyYAML>=6.0
requests>=2.31.0
python-dateutil>=2.8.2
```
