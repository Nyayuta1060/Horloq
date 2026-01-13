# Horloq アーキテクチャドキュメント

> Horloqの設計思想、システム構造、技術スタックの包括的なドキュメントです。  
> プロジェクト全体の理解を深めたい開発者や、コントリビューターにお勧めです。

## 目次

- [システム概要](#システム概要)
- [技術スタック](#技術スタック)
- [アーキテクチャ図](#アーキテクチャ図)
- [ディレクトリ構造](#ディレクトリ構造)
- [コアコンポーネント](#コアコンポーネント)
- [プラグインシステム](#プラグインシステム)
- [データフロー](#データフロー)
- [設計原則](#設計原則)

## システム概要

Horloqは**シングルプロセス**で動作するPythonベースのデスクトップアプリケーションです。

### 主要特徴

- **CustomTkinter**: モダンなGUI（Tkinter拡張）
- **プラグインシステム**: 動的な機能拡張
- **YAML設定**: 人間が読みやすい設定管理
- **クロスプラットフォーム**: Windows, macOS, Linux対応

## 技術スタック

### コア技術
| 分類       | 技術           | 用途                 |
| ---------- | -------------- | -------------------- |
| **言語**   | Python 3.11+   | 本体実装             |
| **GUI**    | CustomTkinter  | モダンなUI           |
| **ビルド** | PyInstaller    | 実行ファイル生成     |
| **CI/CD**  | GitHub Actions | 自動ビルド・リリース |

### 主要ライブラリ
| ライブラリ    | 用途                     |
| ------------- | ------------------------ |
| customtkinter | モダンなTkinterラッパー  |
| Pillow        | 画像処理                 |
| PyYAML        | YAML設定ファイル         |
| requests      | HTTP通信（プラグイン用） |

### 開発ツール
| ツール | 用途                 |
| ------ | -------------------- |
| pytest | ユニットテスト       |
| ruff   | 高速リンター         |
| black  | コードフォーマッター |
| mypy   | 型チェック           |

## システムアーキテクチャ

```
┌────────────────────────────────────────────────┐
│       Python Application (Single Process)      │
│                                                │
│  ┌──────────────────────────────────────────┐  │
│  │      Application Core                    │  │
│  │  - Main Window (CustomTkinter)           │  │
│  │  - Configuration Manager                 │  │
│  │  - Event System                          │  │
│  │  - Theme Manager                         │  │
│  └──────────────────────────────────────────┘  │
│                       ↕                        │
│  ┌──────────────────────────────────────────┐  │
│  │      Plugin System Manager               │  │
│  │  - Plugin Loader (importlib)             │  │
│  │  - Plugin Lifecycle Management           │  │
│  │  - Plugin API Provider                   │  │
│  │  - Hook System                           │  │
│  └──────────────────────────────────────────┘  │
│                       ↕                        │
│  ┌──────────────────────────────────────────┐  │
│  │      UI Components (CustomTkinter)       │  │
│  │  - Clock Display (Digital/Analog)        │  │
│  │  - Settings Window                       │  │
│  │  - Plugin Manager UI                     │  │
│  │  - Widget Container                      │  │
│  └──────────────────────────────────────────┘  │
│                       ↕                        │
│  ┌──────────────────────────────────────────┐  │
│  │      Plugin Widgets                      │  │
│  │  - Weather Widget                        │  │
│  │  - Calendar Widget                       │  │
│  │  - Timer Widget                          │  │
│  │  - Custom Plugins...                     │  │
│  └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
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

## プラグインシステム

### プラグインの基本構造

```
my-plugin/
├── plugin.yaml       # メタデータ（唯一の情報源）
├── __init__.py      # プラグイン本体
├── README.md        # 説明
└── requirements.txt # 依存関係（オプション）
```

### plugin.yaml

```yaml
name: my-plugin
version: 1.0.0
author: Your Name
description: プラグインの説明
min_horloq_version: 0.2.0
```

**重要**: `plugin.yaml`が**唯一の情報源**です。Pythonコードでメタデータを重複定義する必要はありません。

### プラグイン実装例

```python
# __init__.py
from horloq.plugins.base import PluginBase
import customtkinter as ctk

class MyPlugin(PluginBase):
    """プラグイン実装"""
    
    def __init__(self, app_context):
        # plugin.yamlから自動的にメタデータ読み込み
        super().__init__(app_context)
        self.widget = None
    
    def initialize(self) -> bool:
        """初期化処理"""
        print(f"{self.name} initialized!")
        return True
    
    def create_widget(self, parent):
        """ウィジェット作成"""
        frame = ctk.CTkFrame(parent)
        label = ctk.CTkLabel(frame, text="Hello from plugin!")
        label.pack(pady=10)
        return frame
    
    def shutdown(self):
        """終了処理"""
        print(f"{self.name} shutdown")

# プラグインクラスをエクスポート
Plugin = MyPlugin
```

### プラグインライフサイクル

```
1. ロード (load_plugin)
   - plugin.yamlの読み込み
   - Pythonモジュールのインポート
   
2. 初期化 (initialize)
   - プラグイン固有の初期化処理
   
3. 有効化 (enable)
   - ウィジェットの作成と表示
   - イベントリスナーの登録
   
4. 実行中
   - イベント処理
   - ユーザー操作への応答
   
5. 無効化 (disable)
   - イベントリスナーの解除
   - ウィジェットの削除
   
6. アンロード
   - リソースのクリーンアップ
```

### プラグインAPI

プラグインが利用できる主なAPI：

```python
class PluginBase:
    """すべてのプラグインの基底クラス"""
    
    def __init__(self, app_context):
        self.app = app_context           # アプリケーション参照
        self.config = app_context.config # 設定マネージャー
        self.events = app_context.events # イベントシステム
        # メタデータはplugin.yamlから自動読み込み
        self.name = None
        self.version = None
        self.author = None
        self.description = None
    
    # 実装必須メソッド
    def initialize(self) -> bool: ...
    def shutdown(self): ...
    
    # オプショナル
    def create_widget(self, parent): ...
    def on_config_changed(self, key, value): ...
```

## 設定管理

### 設定ファイル構造

```yaml
# ~/.config/horloq/config.yaml
window:
  width: 400
  height: 200
  always_on_top: true
  opacity: 1.0

clock:
  format: "24h"  # または "12h"
  show_seconds: true
  show_date: true
  font_size: 48

theme:
  name: "dark"
  custom_colors:
    bg: "#1a1a1a"
    fg: "#ffffff"

plugins:
  enabled:
    - hello
    - timer
  configs:
    weather:
      api_key: "your-api-key"
      location: "Tokyo"
```

### ConfigManagerの使い方

```python
# 設定の取得（ドット記法）
width = config.get("window.width", 400)
theme = config.get("theme.name", "dark")

# 設定の更新
config.set("window.width", 500)
config.set("plugins.enabled", ["hello", "timer"])

# 設定の保存
config.save()
```

## イベントシステム

### イベント駆動アーキテクチャ

```python
# イベントの発火
events.emit("time_updated", {"time": datetime.now()})

# イベントの購読
def on_time_update(data):
    print(f"Time: {data['time']}")

events.on("time_updated", on_time_update)

# イベントの購読解除
events.off("time_updated", on_time_update)
```

### 標準イベント

| イベント名        | 発火タイミング     | データ         |
| ----------------- | ------------------ | -------------- |
| `app_started`     | アプリ起動完了     | -              |
| `app_closing`     | アプリ終了前       | -              |
| `config_changed`  | 設定変更時         | `{key, value}` |
| `theme_changed`   | テーマ変更時       | `{theme_name}` |
| `plugin_loaded`   | プラグインロード時 | `{plugin_id}`  |
| `plugin_enabled`  | プラグイン有効化時 | `{plugin_id}`  |
| `plugin_disabled` | プラグイン無効化時 | `{plugin_id}`  |
| `time_updated`    | 時刻更新時         | `{time}`       |

## セキュリティ考慮事項

### プラグインの制限

1. **ファイルシステムアクセス**
   - プラグインディレクトリ内のみアクセス可能
   - システムファイルへの書き込み制限

2. **ネットワークアクセス**
   - HTTP/HTTPS通信のみ許可
   - ローカルネットワークスキャン禁止

3. **APIの制限**
   - 提供されたPluginAPIのみ使用可能
   - 内部実装への直接アクセス禁止

## パフォーマンス最適化

### 1. 起動時間の最適化
- プラグインの遅延ロード
- 必要なプラグインのみ初期化
- 設定ファイルのキャッシュ

### 2. メモリ使用量の削減
- 未使用プラグインのアンロード
- イベントリスナーの適切なクリーンアップ
- 画像リソースの最適化

### 3. UI応答性の向上
- 時計更新の最適化（必要最小限のredraw）
- 長時間処理のスレッド化
- after()による非同期UI更新

## 拡張性

### 将来の拡張ポイント

1. **テーマシステムの強化**
   - CSSライクなテーマ記述
   - テーマのホットリロード
   - コミュニティテーマの共有

2. **プラグインマーケットプレイス**
   - GitHub Releases経由でのプラグイン配布
   - 自動更新機能
   - レビュー・評価システム

3. **多言語対応**
   - i18n/l10nサポート
   - プラグインごとの翻訳ファイル
   - 動的言語切り替え

4. **ウィジェットシステムの拡張**
   - カスタムレイアウトエンジン
   - ドラッグ&ドロップによるレイアウト編集
   - ウィジェットのリサイズ・配置カスタマイズ

## 関連ドキュメント

- [開発ガイド](DEVELOPMENT.md) - 開発環境のセットアップと開発フロー
- [プラグイン開発ガイド](PLUGIN_DEVELOPMENT.md) - プラグイン開発の詳細
- [機能仕様書](FEATURES.md) - 実装されている機能の詳細
- [バージョン管理ガイド](VERSION_MANAGEMENT.md) - バージョン管理とリリース手順
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

## 関連ドキュメント

- [開発ガイド](DEVELOPMENT.md) - 開発環境のセットアップと開発フロー
- [プラグイン開発ガイド](PLUGIN_DEVELOPMENT.md) - プラグイン開発の詳細
- [機能仕様書](FEATURES.md) - 実装されている機能の詳細
- [バージョン管理ガイド](VERSION_MANAGEMENT.md) - バージョン管理とリリース手順
