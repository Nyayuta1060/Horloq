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

複数のプラグインを1つのリポジトリで管理する場合、ルートに`plugins.yaml`を配置します。

#### 🚨 重要: plugins.yamlは自動生成してください

`plugins.yaml`は**各プラグインの`plugin.yaml`から自動生成**することを強く推奨します。  
手動でメンテナンスすると、バージョン番号や説明の不整合が発生しやすくなります。

**推奨される自動生成の方法:**

1. **Python スクリプトで生成** ([generate_catalog.py の例](https://github.com/Nyayuta1060/Horloq-plugins/blob/main/generate_catalog.py))
   ```python
   import yaml
   from pathlib import Path
   
   plugins = []
   for plugin_dir in Path(".").iterdir():
       if plugin_dir.is_dir() and (plugin_dir / "plugin.yaml").exists():
           with open(plugin_dir / "plugin.yaml") as f:
               metadata = yaml.safe_load(f)
           plugins.append({
               "name": metadata["name"],
               "path": str(plugin_dir),
               "description": metadata["description"],
               "version": metadata["version"],
               "author": metadata["author"]
           })
   
   catalog = {
       "repository": "username/horloq-plugins",
       "plugins": plugins
   }
   
   with open("plugins.yaml", "w") as f:
       yaml.dump(catalog, f, allow_unicode=True)
   ```

2. **GitHub Actions で自動更新** ([ワークフロー例](https://github.com/Nyayuta1060/Horloq-plugins/blob/main/.github/workflows/generate-catalog.yml))
   ```yaml
   name: Generate Plugin Catalog
   on:
     push:
       paths:
         - '**/plugin.yaml'
   jobs:
     generate:
       runs-on: ubuntu-latest
       permissions:
         contents: write
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
         - run: pip install pyyaml
         - run: python generate_catalog.py
         - run: |
             git config user.name "github-actions[bot]"
             git add plugins.yaml
             git commit -m "Auto-update plugins.yaml" || exit 0
             git push
   ```

**自動生成のメリット:**
- ✅ `plugin.yaml` が Single Source of Truth（唯一の情報源）
- ✅ バージョン番号の不整合を防止
- ✅ プラグイン追加時の手間を削減
- ✅ ヒューマンエラーの削減

**plugins.yaml の例（自動生成後）:**
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
2. ルートに`plugins.yaml`を作成してプラグイン一覧を記載（**自動生成を推奨**）
3. 各プラグインをサブディレクトリに配置
4. READMEにインストール方法を記載

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

## プラグイン更新通知システム

Horloq v0.1.0以降、プラグインの更新を自動的に検知して通知する機能があります。

### ユーザー向け機能

1. **起動時の自動チェック**
   - Horloq起動時にバックグラウンドで更新をチェック
   - 更新があれば画面上部に青いバナーで通知

2. **更新通知バナー**
   ```
   ┌─────────────────────────────────────┐
   │ 🔔 2個のプラグイン更新があります  [詳細を見る] [×] │
   └─────────────────────────────────────┘
   ```

3. **更新詳細ダイアログ**
   - 「詳細を見る」をクリックすると更新可能なプラグインの一覧を表示
   - 現在のバージョン → 最新バージョンを表示
   - ワンクリックで更新可能

4. **プラグイン管理画面からの更新確認**
   - プラグイン管理画面で更新可能なプラグインに「🔄 更新可能」バッジを表示
   - 「更新」ボタンをクリックして最新版にアップデート

### 開発者向け: 更新通知の仕組み

#### バージョン比較

Horloqは以下の方法でプラグインの更新を検知します：

1. **ローカルのバージョン取得**
   - インストール済みプラグインの`plugin.yaml`からバージョンを読み取り

2. **リモートのバージョン取得**
   - GitHubリポジトリから最新の`plugin.yaml`または`plugins.yaml`を取得

3. **セマンティックバージョニング比較**
   ```python
   # 例: 1.0.0 → 1.0.1 は更新あり
   # 例: 1.0.0 → 1.0.0 は更新なし
   ```

#### plugin.yaml のバージョン管理

プラグインを更新する際は、必ず`plugin.yaml`の`version`フィールドを更新してください：

```yaml
name: my-plugin
version: 1.0.1  # ← 必ず更新
author: Your Name
description: 新機能を追加しました
min_horloq_version: 0.1.0
```

**バージョン番号の付け方（セマンティックバージョニング）:**
- `MAJOR.MINOR.PATCH` 形式（例: `1.2.3`）
- **MAJOR**: 互換性のない大きな変更
- **MINOR**: 後方互換性のある機能追加
- **PATCH**: バグ修正

**更新フロー:**
1. プラグインのコードを変更
2. `plugin.yaml`の`version`を更新
3. コミット & プッシュ
4. （モノレポの場合）GitHub Actionsが自動的に`plugins.yaml`も更新
5. ユーザーが次回Horloq起動時に更新通知を受け取る

### 開発者向け: 更新を促す方法

1. **GitHubリリースの作成**
   - GitHubでリリースを作成すると、ユーザーが変更内容を確認しやすくなります

2. **READMEに変更履歴を記載**
   ```markdown
   ## Changelog
   
   ### v1.0.1 (2024-01-15)
   - 🐛 バグ修正: タイマーのリセット機能を修正
   - ✨ 新機能: カスタム時間設定を追加
   ```

3. **破壊的変更の通知**
   - `min_horloq_version`を更新して、必要なHorloqのバージョンを明示

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