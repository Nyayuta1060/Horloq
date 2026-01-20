# バージョン管理 & リリースガイド

> Horloqのバージョン管理とリリース手順の完全ガイドです。  
> バージョン更新、ビルド、GitHub Releasesでの公開まで網羅します。

## 目次

- [バージョン管理の基本](#バージョン管理の基本)
- [バージョン更新手順](#バージョン更新手順)
- [ビルド方法](#ビルド方法)
- [リリース手順](#リリース手順)
- [トラブルシューティング](#トラブルシューティング)

## バージョン管理の基本

###  Single Source of Truth

Horloqでは、**`horloq/__init__.py`の`__version__`がバージョン情報の唯一の情報源**です。

```python
# horloq/__init__.py
__version__ = "0.2.1"
```

##  自動的にバージョンが反映される場所

以下のファイルは`horloq/__init__.py`から自動的にバージョンを読み込みます：

### 1. `setup.py`
```python
# horloq/__init__.py からバージョンを読み込む
init_file = Path(__file__).parent / "horloq" / "__init__.py"
version = None
with open(init_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
```

### 2. `pyproject.toml`
```toml
[project]
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "horloq.__version__"}
```

### 3. アップデートチェッカー
```python
# horloq/core/updater.py
from .. import __version__

class UpdateChecker:
    def __init__(self):
        self.current_version = __version__
```

## バージョン更新手順

新しいバージョンをリリースする際の手順です。

### ステップ1: バージョン番号を決定

セマンティックバージョニング（`MAJOR.MINOR.PATCH`）に従います：

| 変更の種類 | 例            | 説明                     |
| ---------- | ------------- | ------------------------ |
| **MAJOR**  | 1.0.0 → 2.0.0 | 互換性のない大きな変更   |
| **MINOR**  | 0.2.1 → 0.3.0 | 後方互換性のある機能追加 |
| **PATCH**  | 0.2.1 → 0.2.2 | バグ修正                 |

### ステップ2: `horloq/__init__.py` を更新

```python
# 変更前
__version__ = "0.2.1"

# 変更後
__version__ = "0.3.0"
```

**これだけでOK！** 他のファイル（setup.py, pyproject.toml）は自動的に読み込みます。

### ステップ3: バージョンを確認

```bash
# バージョンが正しく反映されているか確認
python -c "import horloq; print(horloq.__version__)"
# → 0.3.0

# setup.py経由でも確認
python setup.py --version
# → 0.3.0
```

### ステップ4: コミット＆タグ

#### 方法1: リリーススクリプトを使用（推奨）

```bash
# スクリプトに実行権限を付与（初回のみ）
chmod +x scripts/release-commit.sh

# スクリプトを実行
./scripts/release-commit.sh

# バージョンを入力
Enter version tag (e.g., v0.3.0): v0.3.0

# スクリプトが自動的に:
# - __init__.py との整合性確認（不一致なら更新を提案）
# - git add horloq/__init__.py
# - git commit -m "chore: bump version to 0.3.0"
# - git tag v0.3.0
# - git push origin main --tags
# を実行します
```

#### 方法2: 手動実行

```bash
git add horloq/__init__.py
git commit -m "chore: bump version to 0.3.0"
git tag v0.3.0
git push origin main --tags
```

## ビルド方法

### ローカルビルド

#### Linux/macOS
```bash
chmod +x scripts/build.sh
./scripts/build.sh
```

#### Windows
```cmd
scripts\build.bat
```

ビルドされたバイナリは `dist/` ディレクトリに作成されます。

### 手動ビルド（PyInstaller）

```bash
# 依存関係をインストール
pip install pyinstaller

# ビルド
pyinstaller build.spec

# 成果物
ls dist/  # horloq または horloq.exe
```

## リリース手順

### 自動リリース（推奨）

タグをプッシュすると、GitHub Actionsが自動的にビルドとドラフトリリースを作成します。

```bash
git tag v0.3.0
git push origin main --tags
```

#### 自動実行される内容

```
タグプッシュ
  ↓
GitHub Actions 起動
  ↓
3つのプラットフォームでビルド:
  - Linux (x86_64)
  - Windows (x86_64)
  - macOS (x86_64)
  ↓
ドラフトリリース作成（自動）
  ↓
手動でリリースノート編集
  ↓
「Publish release」で公開
```

### リリース公開の手順

1. **[Releases ページ](https://github.com/Nyayuta1060/Horloq/releases)を開く**

2. **ドラフトリリースを見つける**
   - `v0.3.0` というタイトルのドラフト

3. **リリースノートを編集**（テンプレートから）
   ```markdown
   ## Horloq v0.3.0
   
   ### 新機能
   - プラグインの自動更新通知
   - Windows環境での依存ライブラリ自動インストール
   
   ### バグ修正
   - タイマープラグインのリセット機能を修正
   
   ### その他の変更
   - ドキュメントを最新化
   
   ###  インストール
   
   #### Windows
   1. `horloq-windows-x86_64-0.3.0.exe` をダウンロード
   2. ダブルクリックで実行
   
   #### Linux
   ```bash
   wget https://github.com/Nyayuta1060/Horloq/releases/download/v0.3.0/horloq-linux-x86_64-0.3.0
   chmod +x horloq-linux-x86_64-0.3.0
   ./horloq-linux-x86_64-0.3.0
   ```
   
   #### macOS
   ```bash
   curl -L -o horloq https://github.com/Nyayuta1060/Horloq/releases/download/v0.3.0/horloq-macos-x86_64-0.3.0
   chmod +x horloq
   ./horloq
   ```
   
   ---
   
   **Full Changelog**: https://github.com/Nyayuta1060/Horloq/compare/v0.2.1...v0.3.0
   ```

4. **ビルド成果物を確認**（バージョン番号付き）
   - horloq-linux-x86_64-0.3.0
   - horloq-windows-x86_64-0.3.0.exe
   - horloq-macos-x86_64-0.3.0

5. **「Publish release」をクリック**

### 手動リリース（非推奨）

自動リリースが使えない場合のみ：

1. ローカルでビルド
2. [GitHub Releases](https://github.com/Nyayuta1060/Horloq/releases/new)で新規作成
3. タグを指定（例: v0.3.0）
4. リリースノート記載
5. ビルド成果物をアップロード

## リリースチェックリスト

新しいバージョンをリリースする際のチェックリスト：

### ローカルでの準備
- [ ] `horloq/__init__.py`の`__version__`を更新
- [ ] `python -c "import horloq; print(horloq.__version__)"` で確認
- [ ] テストがすべてパス: `pytest`
- [ ] ローカルビルドが成功: `pyinstaller build.spec`

### Git操作
- [ ] 変更をコミット: `git commit -m "chore: bump version to X.Y.Z"`
- [ ] タグ作成: `git tag vX.Y.Z`
- [ ] プッシュ: `git push origin main --tags`

### GitHub Actions（自動）
- [ ] ビルドワークフローが成功（3プラットフォーム）
- [ ] ドラフトリリースが作成される

### 手動作業（重要！）
- [ ] [Releases ページ](https://github.com/Nyayuta1060/Horloq/releases)を開く
- [ ] ドラフトリリースを見つける
- [ ] リリースノートを丁寧に編集：
  - 新機能の説明
  - バグ修正の詳細
  - Breaking Changes（あれば）
  - インストール手順
- [ ] ビルド成果物（3つのバイナリ）が添付されているか確認
- [ ] **「Publish release」をクリック**

### 公開後
- [ ] リリースが正しく公開されているか確認
- [ ] ダウンロードリンクが動作するか確認
- [ ] 必要に応じてSNSで告知

## トラブルシューティング

### ビルドエラー

**問題**: `ModuleNotFoundError: No module named 'xxx'`

**解決**:
```bash
pip install -r requirements.txt
pip install pyinstaller
```

**問題**: バイナリが起動しない

**解決**:
- `build.spec` の `hiddenimports` に不足しているモジュールを追加
- `console=True` に変更してエラーメッセージを確認

### GitHub Actions エラー

**問題**: アクションが失敗する

**解決**:
1. Actions タブでログを確認
2. requirements.txt に全ての依存関係が記載されているか確認
3. PyInstallerのバージョンを固定: `pip install pyinstaller==6.3.0`

### バージョン不整合

**問題**: 複数ファイルでバージョンがずれている

**[NG] 間違った方法**:
```python
# setup.py
version = "0.3.0"

# pyproject.toml
version = "0.2.1"

# horloq/__init__.py
__version__ = "0.2.0"
```

**[OK] 正しい方法**:
```python
# horloq/__init__.py のみ更新
__version__ = "0.3.0"

# setup.py と pyproject.toml は自動読み込み
```

## バージョン確認方法

### コマンドライン
```bash
# Python経由
python -c "import horloq; print(horloq.__version__)"

# CLI経由（実装済みの場合）
horloq --version

# setup.py経由
python setup.py --version
```

### プログラム内
```python
import horloq
print(f"Horloq version: {horloq.__version__}")
```

### GitHub Actions
```yaml
- name: Get version
  run: python -c "import horloq; print(horloq.__version__)"
```

## なぜ一元管理が重要か

### 問題点（一元管理しない場合）

```python
# horloq/__init__.py
__version__ = "0.2.1"

# setup.py
version = "0.3.0"  # 不整合！

# pyproject.toml
version = "0.2.0"  # さらに不整合！
```

→ どれが正しいバージョンか分からない！

### 解決策（Single Source of Truth）

```python
# horloq/__init__.py （唯一の真実）
__version__ = "0.2.1"

# setup.py（自動読み込み）
version = load_from_init()  # → "0.2.1"

# pyproject.toml（自動読み込み）
version = {attr = "horloq.__version__"}  # → "0.2.1"
```

→ 常に整合性が保たれる！

## 参考リンク

- [セマンティックバージョニング](https://semver.org/lang/ja/)
- [PEP 440 – Version Identification](https://peps.python.org/pep-0440/)
- [setuptools dynamic metadata](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html#dynamic-metadata)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [GitHub Actions Documentation](https://docs.github.com/ja/actions)
