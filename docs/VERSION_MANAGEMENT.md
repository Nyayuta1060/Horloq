# バージョン管理ガイド

## 📌 バージョンの唯一の情報源（Single Source of Truth）

Horloqプロジェクトでは、**`horloq/__init__.py`の`__version__`がバージョン情報の唯一の情報源**です。

```python
# horloq/__init__.py
__version__ = "0.2.1"
```

## 🔄 自動的にバージョンが反映される場所

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

## 📝 バージョンの更新手順

新しいバージョンをリリースする際は、以下の手順で行います：

### 1. バージョン番号を決定

セマンティックバージョニング（`MAJOR.MINOR.PATCH`）に従います：

- **MAJOR**: 互換性のない大きな変更（例: 1.0.0 → 2.0.0）
- **MINOR**: 後方互換性のある機能追加（例: 0.2.1 → 0.3.0）
- **PATCH**: バグ修正（例: 0.2.1 → 0.2.2）

### 2. `horloq/__init__.py` のみを更新

```python
# 変更前
__version__ = "0.2.1"

# 変更後
__version__ = "0.3.0"
```

**これだけでOK！** 他のファイルは自動的に更新されます。

### 3. 変更を確認

```bash
# バージョンが反映されているか確認
python -c "import horloq; print(horloq.__version__)"

# setup.py経由でも確認
python setup.py --version
```

### 4. コミット＆タグ

```bash
git add horloq/__init__.py
git commit -m "chore: bump version to 0.3.0"
git tag v0.3.0
git push origin main --tags
```

### 5. GitHub Releasesで公開

1. GitHubの「Releases」ページへ
2. 「Draft a new release」をクリック
3. タグ: `v0.3.0` を選択
4. リリースノートを記載
5. バイナリファイルを添付（オプション）
6. 「Publish release」をクリック

## ⚠️ やってはいけないこと

### ❌ 複数ファイルのバージョンを直接編集

```python
# ❌ これはやらない
# setup.py
version="0.3.0"

# pyproject.toml
version = "0.3.0"

# horloq/__init__.py
__version__ = "0.3.0"
```

これをすると、同期が取れなくなります。

### ✅ 正しい方法

```python
# ✅ これだけでOK
# horloq/__init__.py
__version__ = "0.3.0"
```

## 🔍 バージョン確認方法

### コマンドライン
```bash
# Python経由
python -c "import horloq; print(horloq.__version__)"

# CLI経由
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

## 📦 リリースチェックリスト

新しいバージョンをリリースする際のチェックリスト：

- [ ] `horloq/__init__.py`の`__version__`を更新
- [ ] CHANGELOGに変更内容を記載
- [ ] `python -c "import horloq; print(horloq.__version__)"` で確認
- [ ] テストがすべてパス: `pytest`
- [ ] ビルドが成功: `pyinstaller horloq.spec`
- [ ] コミット: `git commit -m "chore: bump version to X.Y.Z"`
- [ ] タグ作成: `git tag vX.Y.Z`
- [ ] プッシュ: `git push origin main --tags`
- [ ] GitHub Releasesで公開
- [ ] リリースノートに変更内容を記載

## 🎯 なぜ一元管理が重要か

### 問題点（一元管理しない場合）

```python
# horloq/__init__.py
__version__ = "0.2.1"

# setup.py
version = "0.3.0"  # 😱 不整合！

# pyproject.toml
version = "0.2.0"  # 😱 さらに不整合！
```

→ どれが正しいバージョンか分からない！

### 解決策（一元管理）

```python
# horloq/__init__.py （唯一の真実）
__version__ = "0.2.1"

# setup.py（自動読み込み）
version = load_from_init()  # → "0.2.1"

# pyproject.toml（自動読み込み）
version = {attr = "horloq.__version__"}  # → "0.2.1"
```

→ 常に整合性が保たれる！

## 🔗 関連ドキュメント

- [セマンティックバージョニング](https://semver.org/lang/ja/)
- [PEP 440 – Version Identification](https://peps.python.org/pep-0440/)
- [setuptools dynamic metadata](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html#dynamic-metadata)
