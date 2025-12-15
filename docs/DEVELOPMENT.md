# Horloq 開発ガイド

## 開発環境のセットアップ

### 必要要件
- Python 3.11 以上
- pip または poetry
- Git

### 初期セットアップ

```bash
# リポジトリのクローン
git clone https://github.com/Nyayuta1060/Horloq.git
cd Horloq

# 仮想環境の作成（推奨）
python -m venv venv

# 仮想環境の有効化
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# または Poetry を使用
poetry install

# 開発モードで起動
python -m horloq
```

## プロジェクト構造の理解

```
horloq/
├── horloq/                # メインパッケージ
│   ├── core/             # コア機能
│   ├── ui/               # UIコンポーネント
│   ├── plugins/          # プラグインシステム
│   └── utils/            # ユーティリティ
├── plugins/              # 標準プラグイン
├── resources/            # リソース（アイコン等）
├── docs/                 # ドキュメント
└── tests/                # テストコード
```

## 開発ワークフロー

### ブランチ戦略

```
main          # 本番リリース用
  ├─ develop  # 開発統合ブランチ
      ├─ feature/xxx    # 新機能開発
      ├─ bugfix/xxx     # バグ修正
      └─ plugin/xxx     # プラグイン開発
```

### コミットメッセージ規約

Conventional Commits を採用：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type:**
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマット等）
- `refactor`: リファクタリング
- `perf`: パフォーマンス改善
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更
- `build`: ビルドシステムの変更

**例:**
```
feat(clock): add analog clock display mode

Implement analog clock display with customizable design options.
Includes hour, minute, and second hands with smooth animation.

Closes #123
```

## コーディング規約

### Python スタイルガイド

PEP 8 に準拠し、以下のツールを使用します：
- **Black**: コードフォーマッター
- **Ruff**: 高速リンター
- **mypy**: 型チェック

#### 命名規則
- **クラス**: PascalCase (`PluginManager`)
- **関数・変数**: snake_case (`load_plugin`, `is_enabled`)
- **定数**: UPPER_SNAKE_CASE (`MAX_PLUGINS`, `DEFAULT_THEME`)
- **プライベート**: アンダースコアプレフィックス (`_internal_method`)

#### 型ヒント
すべての関数に型ヒントを追加：

```python
# Good
def load_plugin(plugin_id: str) -> Optional[Plugin]:
    """プラグインをロードする"""
    ...

class PluginManager:
    def __init__(self, plugin_dir: Path, config: ConfigManager) -> None:
        self.plugins: Dict[str, Plugin] = {}
    
    def enable_plugin(self, plugin_id: str) -> None:
        ...

# Bad
def load_plugin(id):  # NG: 型ヒントなし
    ...

class pluginmanager:  # NG: 命名規則違反
    def __init__(self, dir, cfg):  # NG: 型ヒントなし
        self.plugins = {}  # NG: 型注釈なし
```

## プラグイン開発

### プラグインの作成

#### 1. プラグインディレクトリの作成

```bash
mkdir plugins/my-plugin
cd plugins/my-plugin
```

#### 2. manifest.yaml の作成

```yaml
# manifest.yaml
id: my-plugin
name: My Plugin
version: 1.0.0
description: 私の素晴らしいプラグイン
author: Your Name
main: plugin.py
permissions:
  - network
  - notifications
```

#### 3. プラグインコードの作成

```python
# plugin.py
import customtkinter as ctk
from horloq.plugins.base import PluginBase
from horloq.plugins.api import PluginAPI

class Plugin(PluginBase):
    """My Plugin の実装"""
    
    def __init__(self, api: PluginAPI):
        super().__init__(api)
        self.widget = None
    
    def activate(self) -> None:
        """プラグイン有効化時の処理"""
        print(f"MyPlugin activated!")
        
        # ウィジェットの作成
        self.widget = self.create_widget()
        
        # UIに追加
        self.api.ui.add_widget(self.widget)
        
        # イベントリスナーの登録
        self.api.events.on('time_update', self.on_time_update)
    
    def deactivate(self) -> None:
        """プラグイン無効化時の処理"""
        # イベントリスナーの解除
        self.api.events.off('time_update', self.on_time_update)
        
        # ウィジェットの削除
        if self.widget:
            self.api.ui.remove_widget(self.widget)
        
        print(f"MyPlugin deactivated!")
    
    def create_widget(self) -> ctk.CTkFrame:
        """ウィジェットの作成"""
        frame = ctk.CTkFrame(None)
        
        label = ctk.CTkLabel(
            frame,
            text="My Plugin Widget",
            font=("Arial", 16)
        )
        label.pack(padx=10, pady=10)
        
        return frame
    
    def on_time_update(self, time):
        """時刻更新時の処理"""
        # 時刻が更新されるたびに呼ばれる
        pass
```

#### 4. テストとデバッグ

```bash
# プラグインのテスト
python -m pytest tests/test_plugins/test_my_plugin.py

# アプリを起動してプラグインを有効化
python -m horloq
```

### プラグインAPI リファレンス

#### UI API

```python
# 通知の表示
api.ui.show_notification('タイトル', 'メッセージ')

# ウィジェットの追加
widget = create_my_widget()
api.ui.add_widget(widget)

# ウィジェットの削除
api.ui.remove_widget(widget)
```

#### Storage API

```python
# データの保存
api.storage.set('key', {'foo': 'bar'})

# データの取得
data = api.storage.get('key')
# => {'foo': 'bar'}

# デフォルト値付きで取得
value = api.storage.get('missing_key', default='default_value')

# データの削除
api.storage.delete('key')
```

#### HTTP API

```python
# GETリクエスト
response = api.http.get('https://api.example.com/data')
data = response.json()

# POSTリクエスト
response = api.http.post('https://api.example.com/data', {
    'foo': 'bar',
})
```

#### System API

```python
# 現在時刻の取得
now = api.system.get_time()
# => datetime object

# 位置情報の取得（location権限が必要）
location = api.system.get_location()
# => (latitude, longitude)
```

#### Events API

```python
# イベントリスナーの登録
def on_time_update(time):
    print(f'Time updated: {time}')

api.events.on('time_update', on_time_update)

# イベントの発火
api.events.emit('custom-event', {'data': 'foo'})

# イベントリスナーの解除
api.events.off('time_update', on_time_update)
```

## テスト

### ユニットテストの実行

```bash
# すべてのテストを実行
pytest

# 特定のファイルをテスト
pytest tests/test_core/test_config.py

# カバレッジレポート付きで実行
pytest --cov=horloq --cov-report=html

# カバレッジレポートの表示
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### テストの書き方

```python
# tests/test_core/test_config.py
import pytest
from pathlib import Path
from horloq.core.config import ConfigManager

def test_config_default_values(tmp_path):
    """デフォルト値が正しく設定されているか"""
    config_file = tmp_path / "config.yaml"
    config = ConfigManager(config_file)
    
    assert config.get("window.width") == 400
    assert config.get("window.height") == 200
    assert config.get("clock.format") == "24h"

def test_config_set_and_get(tmp_path):
    """設定の保存と取得が正しく動作するか"""
    config_file = tmp_path / "config.yaml"
    config = ConfigManager(config_file)
    
    config.set("clock.format", "12h")
    assert config.get("clock.format") == "12h"
    
    config.save()
    
    # 再ロード
    config2 = ConfigManager(config_file)
    assert config2.get("clock.format") == "12h"

def test_config_nested_keys(tmp_path):
    """ネストされたキーが正しく動作するか"""
    config_file = tmp_path / "config.yaml"
    config = ConfigManager(config_file)
    
    config.set("theme.custom_colors.bg", "#ff0000")
    assert config.get("theme.custom_colors.bg") == "#ff0000"
```

## ビルドとパッケージング

### 開発ビルド

```bash
# 依存関係の確認
pip check

# コードフォーマット
black horloq/

# リンター実行
ruff check horloq/

# 型チェック
mypy horloq/
```

### PyInstallerでのビルド

```bash
# 単一EXEファイルの作成
pyinstaller horloq.spec

# ビルド結果の確認
ls dist/

# 実行
./dist/Horloq  # Linux/Mac
dist\Horloq.exe  # Windows
```

### クロスプラットフォームビルド

```bashyaml の構文エラー
- Pythonファイルの構文エラー
- Plugin クラスが定義されていない

**解決方法:**
```bash
# YAMLの構文チェック
python -c "import yaml; yaml.safe_load(open('plugins/my-plugin/manifest.yaml'))"

# Pythonファイルの構文チェック
python -m py_compile plugins/my-plugin/plugin.py

# ログを確認
tail -f ~/.config/horloq/logs/horloq.log  # Linux
tail -f ~/Library/Application\ Support/horloq/logs/horloq.log  # macOS
type %APPDATA%\horloq\logs\horloq.log  # Windows
```

#### 2. CustomTkinterのテーマが適用されない

**原因:**
- テーマファイルが見つからない
- CustomTkinterのバージョンが古い

**解決方法:**
```bash
# CustomTkinterを最新版に更新
pip install --upgrade customtkinter

# テーマファイルの確認
ls resources/themes/
```

#### 3. PyInstallerビルドが失敗する

**原因:**
- 隠れた依存関係
- パスの問題

**解決方法:**
```bash
# キャッシュをクリア
pyinstaller --clean horloq.spec

# ビルドログを確認
pyinstaller --log-level DEBUG horloq.spec

# 足りないモジュールを hiddenimports に追加
# horloq.spec の hiddenimports リストに追加
```

#### 4. 仮想環境の問題

**解決方法:**
```bash
# 仮想環境を削除して再作成
rm -rf venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## GitHub Releaseでの公開

### リリースプロセス

#### 1. バージョンの更新

```python
# horloq/__init__.py
__version__ = "1.0.0"
```

```toml
# pyproject.toml
[tool.poetry]
version = "1.0.0"
```

#### 2. CHANGELOG の更新

```markdown
# CHANGELOG.md

## [1.0.0] - 2025-12-15

### Added
- デジタル時計表示機能
- アナログ時計表示機能
- プラグインシステム
- 天気プラグイン
- カレンダープラグイン

### Changed
- UI をCustomTkinterに変更

### Fixed
- 設定の保存に関するバグを修正
```

#### 3. Git タグの作成とプッシュ

```bash
# すべての変更をコミット
git add .
git commit -m "chore: release v1.0.0"

# タグを作成
git tag -a v1.0.0 -m "Release version 1.0.0"

# リモートにプッシュ
git push origin main
git push origin v1.0.0
```

#### 4. GitHub Actions による自動ビルド

タグをプッシュすると、GitHub Actionsが自動的に：
1. Windows, macOS, Linux でビルド
2. 実行ファイルを作成
3. GitHub Releases に公開

#### 5. リリースノートの編集

GitHub Releasesページで：
1. 自動作成されたリリースを編集
2. CHANGELOG の内容を追加
3. スクリーンショットやデモGIFを追加

### リリースの確認

```bash
# リリースページを開く
open https://github.com/Nyayuta1060/Horloq/releases

# ダウンロードリンクの確認
curl -s https://api.github.com/repos/Nyayuta1060/Horloq/releases/latest | \
  jq -r '.assets[].browser_download_url'
```

## コントリビューション

### Pull Request の作成手順

1. Issue を作成（機能追加・バグ報告）
2. ブランチを作成（`feature/xxx` または `bugfix/xxx`）
3. コードを実装
4. テストを追加・実行
5. コードフォーマットとリンターを実行
6. コミット（Conventional Commits形式）
7. Pull Request を作成
8. レビュー対応
9. マージ

### コードレビューのチェックリスト

- [ ] コーディング規約に従っているか
- [ ] 型ヒントが適切に付与されているか
- [ ] テストが追加されているか
- [ ] ドキュメントが更新されているか
- [ ] パフォーマンスへの影響はないか
- [ ] セキュリティ上の問題はないか
- [ ] Black/Ruff でフォーマット済みか

### 開発前の確認

```bash
# コードフォーマット
black horloq/ tests/ plugins/

# リンター
ruff check horloq/ tests/ plugins/

# 型チェック
mypy horloq/

# テスト
pytest

# すべてをまとめて実行
./scripts/check.sh  # または
make check
```

## リソース

### 公式ドキュメント
- [Python Documentation](https://docs.python.org/3/)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [PyInstaller Documentation](https://pyinstaller.org/)

### 関連ツール
- [Black - Code Formatter](https://black.readthedocs.io/)
- [Ruff - Fast Linter](https://beta.ruff.rs/docs/)
- [pytest - Testing Framework](https://docs.pytest.org/)
- [mypy - Type Checker](https://mypy.readthedocs.io/)

### コミュニティ
- GitHub Issues: バグ報告・機能リクエスト
- GitHub Discussions: 質問・議論
- Stack Overflow: `#horloq` タグ
```python
# printデバッグ
print(f"Debug: {variable}")

# ブレークポイント
import pdb; pdb.set_trace()

# より高機能なデバッガ
import ipdb; ipdb.set_trace()

# ログ出力
from horloq.utils.logger import get_logger
logger = get_logger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## トラブルシューティング

### よくある問題

#### 1. プラグインが読み込まれない

**原因:**
- manifest.json の構文エラー
- 権限が不足している
- ファイルパスが間違っている

**解決方法:**
```bash
# ログを確認
tail -f ~/Library/Application\ Support/Horloq/logs/combined.log  # macOS
tail -f ~/.config/Horloq/logs/combined.log                      # Linux
type %APPDATA%\Horloq\logs\combined.log                         # Windows
```

#### 2. IPC通信が失敗する

**原因:**
- チャネル名の不一致
- 型の不整合

**解決方法:**
- `shared/types/ipc.ts` でチャネル定義を確認
- TypeScriptの型エラーをチェック

#### 3. ビルドエラー

**解決方法:**
```bash
# node_modules を削除して再インストール
rm -rf node_modules package-lock.json
npm install

# キャッシュをクリア
npm cache clean --force
```

## コントリビューション

### Pull Request の作成手順

1. Issue を作成（機能追加・バグ報告）
2. ブランチを作成（`feature/xxx` または `bugfix/xxx`）
3. コードを実装
4. テストを追加・実行
5. コミット（Conventional Commits形式）
6. Pull Request を作成
7. レビュー対応
8. マージ

### コードレビューのチェックリスト

- [ ] コーディング規約に従っているか
- [ ] テストが追加されているか
- [ ] ドキュメントが更新されているか
- [ ] 型定義が適切か
- [ ] パフォーマンスへの影響はないか
- [ ] セキュリティ上の問題はないか

## リソース

### 公式ドキュメント
- [Electron Documentation](https://www.electronjs.org/docs)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### 関連ツール
- [Electron Forge](https://www.electronforge.io/)
- [Electron Builder](https://www.electron.build/)
- [Spectron](https://www.electronjs.org/spectron)

### コミュニティ
- GitHub Issues
- Discord Server
- Stack Overflow (#horloq)
