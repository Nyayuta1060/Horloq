# Horloq プラグイン開発ガイド

## プラグインの作り方

### 1. プラグインの構造

#### 単一プラグイン
```
horloq-plugin-example/
├── plugin.yaml          # プラグインのメタデータ
├── __init__.py         # プラグイン本体
├── README.md           # 説明
└── requirements.txt    # 依存関係（オプション）
```

#### モノレポ（複数プラグイン）
```
horloq-plugins/
├── plugins.yaml        # プラグインカタログ
├── weather/
│   ├── plugin.yaml
│   └── __init__.py
├── calendar/
│   ├── plugin.yaml
│   └── __init__.py
└── notes/
    ├── plugin.yaml
    └── __init__.py
```

### 2. plugin.yaml

```yaml
name: example
version: 1.0.0
author: Your Name
description: サンプルプラグイン
min_horloq_version: 0.1.0
```

**重要**: `plugin.yaml`がプラグインメタデータの**唯一の情報源**です。  
Pythonコード内で`name`、`version`、`author`、`description`を指定する必要はありません。  
`PluginBase`のコンストラクタが自動的に`plugin.yaml`からメタデータを読み込みます。

### 3. plugins.yaml（モノレポの場合）

複数のプラグインを1つのリポジトリで管理する場合、ルートに`plugins.yaml`を配置します：

```yaml
repository: username/horloq-plugins
plugins:
  - name: weather
    path: weather
    description: 天気予報を表示
    version: 1.0.0
    author: Your Name
  
  - name: calendar
    path: calendar
    description: カレンダーを表示
    version: 1.0.0
    author: Your Name
  
  - name: notes
    path: notes
    description: メモ機能
    version: 1.0.0
    author: Your Name
```

### 4. __init__.py

```python
from horloq.plugins.base import PluginBase
import customtkinter as ctk


class ExamplePlugin(PluginBase):
    """サンプルプラグイン"""
    
    def __init__(self, app_context):
        # plugin.yamlから自動的にメタデータを読み込みます
        # name, version, author, description は指定不要です
        super().__init__(app_context)
    
    def initialize(self) -> bool:
        """初期化"""
        # 初期化処理
        return True
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        label = ctk.CTkLabel(
            frame,
            text="Hello from plugin!",
            font=("Arial", 14),
        )
        label.pack(pady=10)
        
        return frame
    
    def shutdown(self):
        """終了処理"""
        pass


# プラグインクラスをエクスポート
Plugin = ExamplePlugin
```

## プラグインのインストール方法

### ユーザー向け

#### GUIから（単一プラグイン）
1. Horloqを起動
2. 右クリックメニューから「プラグイン管理」を選択
3. 「GitHubからインストール」ボタンをクリック
4. リポジトリURLまたは`username/repo-name`を入力

#### GUIから（カタログ選択）
1. Horloqを起動
2. 右クリックメニューから「プラグイン管理」を選択
3. 「カタログから選択」ボタンをクリック
4. リポジトリURL（例: `username/horloq-plugins`）を入力
5. 読み込まれたプラグイン一覧から選択してインストール

#### CLIから
```bash
# 単一プラグイン
python -m horloq plugin install username/horloq-plugin-example

# モノレポからサブディレクトリ指定
python -m horloq plugin install username/horloq-plugins:weather

# アンインストール
python -m horloq plugin uninstall weather

# インストール済みプラグイン一覧
python -m horloq plugin list
```

## プラグインの配布

### 単一プラグインの配布

1. GitHubでリポジトリを作成
2. リポジトリ名は `horloq-plugin-xxx` の形式を推奨
3. 上記の構造でファイルを作成
4. READMEにインストール方法を記載

```bash
# インストールコマンドをREADMEに記載
python -m horloq plugin install yourusername/horloq-plugin-example
```

### モノレポでの配布（複数プラグイン）

複数のプラグインを1つのリポジトリで管理する場合：

1. GitHubでリポジトリを作成（例: `horloq-plugins`）
2. ルートに`plugins.yaml`を作成してプラグイン一覧を記載
3. 各プラグインをサブディレクトリに配置
4. READMEにインストール方法を記載

```yaml
# plugins.yaml
repository: username/horloq-plugins
plugins:
  - name: weather
    path: weather
    description: 天気予報プラグイン
  - name: calendar
    path: calendar
    description: カレンダープラグイン
```

**ユーザーの使い方：**

```bash
# CLI: 特定のプラグインをインストール
python -m horloq plugin install username/horloq-plugins:weather

# GUI: カタログから選択してインストール
# 1. プラグイン管理 → カタログから選択
# 2. username/horloq-plugins を入力
# 3. 一覧から選んでインストール
```

**メリット：**
- リポジトリ1つで複数のプラグインを管理
- ユーザーは必要なプラグインだけ選択可能
- プラグインの更新やメンテナンスが楽

## アプリケーションコンテキスト

プラグインは以下のコンテキストにアクセスできます：

```python
self.app_context = {
    "config": ConfigManager,    # 設定管理
    "events": EventManager,     # イベント管理
    "themes": ThemeManager,     # テーマ管理
}
```

### イベントの使用例

```python
def initialize(self):
    # イベントを購読
    self.app_context["events"].on("theme_changed", self._on_theme_changed)
    return True

def _on_theme_changed(self, event):
    # テーマ変更時の処理
    print("Theme changed!")
```

## 公式プラグイン
詳細は [公式プラグイン週](https://github.com/Nyayuta1060/Horloq-Plugins)を確認してください