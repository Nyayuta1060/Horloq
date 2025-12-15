# Horloq アーキテクチャ設計

## 概要
Horloqは、拡張可能なデスクトップ据え置き時計アプリケーションです。プラグインシステムにより、ユーザーが自由に機能を追加・カスタマイズできる設計を採用しています。

## 技術スタック

### コア技術
- **言語**: Python 3.11+
- **GUIフレームワーク**: CustomTkinter (モダンなTkinter拡張)
- **プラグインシステム**: Pythonモジュールベース

### 主要ライブラリ
- **CustomTkinter**: モダンなUI
- **Pillow**: 画像処理
- **requests**: HTTP通信（プラグイン用）
- **python-dateutil**: 日時処理
- **pyyaml**: 設定ファイル管理

### 配布・ビルド
- **PyInstaller**: EXE化
- **GitHub Actions**: CI/CD
- **GitHub Releases**: 配布

### 開発ツール
- **パッケージマネージャー**: pip, poetry
- **テスト**: pytest
- **リンター**: ruff, pylint
- **フォーマッター**: black
- **型チェック**: mypy

## システムアーキテクチャ

```
┌─────────────────────────────────────────────────┐
│          Python Application (Single Process)    │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │      Application Core                    │  │
│  │  - Main Window (CustomTkinter)          │  │
│  │  - Configuration Manager                 │  │
│  │  - Event System                          │  │
│  │  - Theme Manager                         │  │
│  └──────────────────────────────────────────┘  │
│                       ↕                          │
│  ┌──────────────────────────────────────────┐  │
│  │      Plugin System Manager               │  │
│  │  - Plugin Loader (importlib)             │  │
│  │  - Plugin Lifecycle Management           │  │
│  │  - Plugin API Provider                   │  │
│  │  - Hook System                           │  │
│  └──────────────────────────────────────────┘  │
│                       ↕                          │
│  ┌──────────────────────────────────────────┐  │
│  │      UI Components (CustomTkinter)       │  │
│  │  - Clock Display (Digital/Analog)        │  │
│  │  - Settings Window                       │  │
│  │  - Plugin Manager UI                     │  │
│  │  - Widget Container                      │  │
│  └──────────────────────────────────────────┘  │
│                       ↕                          │
│  ┌──────────────────────────────────────────┐  │
│  │      Plugin Widgets                      │  │
│  │  - Weather Widget                        │  │
│  │  - Calendar Widget                       │  │
│  │  - Timer Widget                          │  │
│  │  - Custom Plugins...                     │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## ディレクトリ構造

```
horloq/
├── horloq/                      # メインパッケージ
│   ├── __init__.py
│   ├── __main__.py             # エントリーポイント
│   │
│   ├── core/                    # コア機能
│   │   ├── __init__.py
│   │   ├── app.py              # メインアプリケーション
│   │   ├── window.py           # ウィンドウ管理
│   │   ├── config.py           # 設定管理
│   │   ├── events.py           # イベントシステム
│   │   └── theme.py            # テーマ管理
│   │
│   ├── ui/                      # UIコンポーネント
│   │   ├── __init__.py
│   │   ├── clock.py            # 時計表示
│   │   ├── digital_clock.py    # デジタル時計
│   │   ├── analog_clock.py     # アナログ時計
│   │   ├── settings.py         # 設定画面
│   │   ├── plugin_manager.py   # プラグイン管理UI
│   │   └── widgets.py          # 共通ウィジェット
│   │
│   ├── plugins/                 # プラグインシステム
│   │   ├── __init__.py
│   │   ├── manager.py          # プラグインマネージャー
│   │   ├── loader.py           # プラグインローダー
│   │   ├── api.py              # プラグインAPI
│   │   ├── base.py             # プラグイン基底クラス
│   │   └── hooks.py            # フックシステム
│   │
│   └── utils/                   # ユーティリティ
│       ├── __init__.py
│       ├── constants.py        # 定数
│       ├── helpers.py          # ヘルパー関数
│       └── logger.py           # ロギング
│
├── plugins/                     # 標準プラグイン
│   ├── weather/                # 天気プラグイン
│   │   ├── __init__.py
│   │   ├── plugin.py
│   │   └── manifest.yaml
│   ├── calendar/               # カレンダープラグイン
│   │   ├── __init__.py
│   │   ├── plugin.py
│   │   └── manifest.yaml
│   ├── timer/                  # タイマープラグイン
│   │   ├── __init__.py
│   │   ├── plugin.py
│   │   └── manifest.yaml
│   └── stopwatch/              # ストップウォッチプラグイン
│       ├── __init__.py
│       ├── plugin.py
│       └── manifest.yaml
│
├── tests/                       # テスト
│   ├── __init__.py
│   ├── test_core/
│   ├── test_ui/
│   └── test_plugins/
│
├── docs/                        # ドキュメント
├── resources/                   # リソースファイル
│   ├── icons/                  # アイコン
│   └── themes/                 # テーマファイル
│
├── dist/                        # ビルド出力（.gitignore）
├── build/                       # ビルド一時ファイル（.gitignore）
│
├── .github/
│   └── workflows/
│       ├── build.yml           # ビルドワークフロー
│       └── release.yml         # リリースワークフロー
│
├── pyproject.toml              # Poetryプロジェクト設定
├── requirements.txt            # 依存関係
├── horloq.spec                 # PyInstallerスペックファイル
├── .gitignore
└── README.md
```

## コアコンポーネント

### 1. Application Core (core/app.py)
- Tkinterメインループの管理
- ウィンドウの作成と管理
- アプリケーション設定の読み込み・保存
- イベントディスパッチャー

### 2. Plugin System Manager (plugins/manager.py)
- プラグインの検索とロード（importlib使用）
- プラグインのライフサイクル管理（初期化、有効化、無効化、アンロード）
- フックシステムによるプラグイン間通信
- プラグインAPIの提供

### 3. UI Layer (ui/)
- CustomTkinterベースのモダンなUI
- 時計表示（デジタル/アナログ切り替え可能）
- 設定ウィンドウ（Toplevel）
- プラグイン管理UI
- テーマカスタマイズ

### 4. Configuration System (core/config.py)
- YAMLファイルでの設定管理
- ユーザー設定の永続化（~/.horloq/config.yaml）
- デフォルト設定の管理
- 設定のバリデーション
- 型安全なアクセス

### 5. Event System (core/events.py)
- Observer パターンによるイベント管理
- カスタムイベントの発火と購読
- プラグイン間の疎結合な通信

## データフロー

```
User Action (UI Event)
    ↓
Event Handler (Tkinter Callback)
    ↓
Core Logic / Plugin System
    ↓
Event Emission
    ↓
Event Subscribers (UI Components / Plugins)
    ↓
UI Update (widget.configure() / after())
```

### 具体例: 設定変更のフロー

```
1. ユーザーが設定ウィンドウで変更
   → settings.py の on_save_click()

2. ConfigManager.set(key, value)
   → config.yaml への保存

3. EventSystem.emit('config_changed', {key, value})

4. 各コンポーネントが購読
   → ClockWidget.on_config_changed()
   → ThemeManager.on_config_changed()

5. UI更新
   → self.clock_label.configure(text=new_format)
```

## プラグインシステム設計

### プラグインの構造
各プラグインは以下の構造を持ちます：

```python
# manifest.yaml
id: my-plugin
name: My Plugin
version: 1.0.0
description: プラグインの説明
author: 作者名
main: plugin.py
permissions:
  - network
  - notifications
```

```python
# plugin.py
from horloq.plugins.base import PluginBase
from horloq.plugins.api import PluginAPI

class MyPlugin(PluginBase):
    def __init__(self, api: PluginAPI):
        super().__init__(api)
        self.widget = None
    
    def activate(self) -> None:
        """プラグイン有効化時に呼ばれる"""
        self.widget = self.create_widget()
        self.api.ui.add_widget(self.widget)
        self.api.events.on('time_update', self.on_time_update)
    
    def deactivate(self) -> None:
        """プラグイン無効化時に呼ばれる"""
        self.api.events.off('time_update', self.on_time_update)
        if self.widget:
            self.api.ui.remove_widget(self.widget)
    
    def on_time_update(self, time):
        # 時刻更新時の処理
        pass
```

### プラグインAPI
プラグインが利用できるAPIを提供：

```python
class PluginAPI:
    """プラグインが使用できるAPI"""
    
    def __init__(self, plugin_id: str):
        self.plugin_id = plugin_id
        self.ui = UIApi(plugin_id)
        self.storage = StorageApi(plugin_id)
        self.http = HttpApi(plugin_id)
        self.system = SystemApi(plugin_id)
        self.events = EventApi(plugin_id)

class UIApi:
    """UI操作API"""
    def show_notification(self, message: str) -> None: ...
    def add_widget(self, widget: tk.Widget) -> None: ...
    def remove_widget(self, widget: tk.Widget) -> None: ...

class StorageApi:
    """データストレージAPI"""
    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def delete(self, key: str) -> None: ...

class HttpApi:
    """HTTP通信API（権限必要）"""
    def get(self, url: str) -> requests.Response: ...
    def post(self, url: str, data: dict) -> requests.Response: ...

class SystemApi:
    """システム情報API"""
    def get_time(self) -> datetime: ...
    def get_location(self) -> tuple[float, float]: ...  # 権限必要

class EventApi:
    """イベントAPI"""
    def on(self, event: str, callback: Callable) -> None: ...
    def off(self, event: str, callback: Callable) -> None: ...
    def emit(self, event: str, data: Any) -> None: ...
```

## セキュリティ考慮事項

1. **プラグインのサンドボックス化**
   - プラグインは制限されたAPIのみアクセス可能
   - 明示的な権限モデル

2. **IPC通信の検証**
   - すべてのIPC通信でデータバリデーション
   - 型安全な通信

3. **外部リソースのアクセス制御**
   - ネットワークアクセスは権限が必要
   - ファイルシステムアクセスの制限

## パフォーマンス考慮事項

1. **レンダリング最適化**
   - 時計の更新は必要最小限に
   - React.memo や useMemo の活用

2. **プラグインの遅延ロード**
   - 必要なプラグインのみロード
   - 非同期初期化

3. **メモリ管理**
   - 未使用プラグインのアンロード
   - イベントリスナーの適切なクリーンアップ

## 拡張性

1. **テーマシステム**
   - CSS変数によるカスタマイズ
   - テーマプラグインのサポート

2. **ウィジェットシステム**
   - プラグインがカスタムウィジェットを追加可能
   - レイアウトのカスタマイズ

3. **多言語対応**
   - i18n対応
   - プラグインごとの翻訳ファイル
