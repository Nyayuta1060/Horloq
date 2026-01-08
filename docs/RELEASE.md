# リリースガイド

## バイナリファイルの作成

### ローカルでのビルド

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

### PyInstallerの手動実行

```bash
# 依存関係をインストール
pip install pyinstaller

# ビルド
pyinstaller build.spec
```

## GitHub Releaseの作成

### 自動リリース（推奨）

1. バージョンタグを作成してプッシュ:
```bash
git tag v0.1.0
git push origin v0.1.0
```

2. GitHub Actionsが自動的に:
   - Linux、Windows、macOS用のバイナリをビルド
   - GitHub Releaseを作成
   - バイナリをアップロード

### 手動リリース

1. ローカルでビルド:
```bash
./scripts/build.sh  # Linux/macOS
# または
scripts\build.bat   # Windows
```

2. GitHubのリリースページへ:
   - https://github.com/Nyayuta1060/Horloq/releases/new
   - タグを作成（例: v0.1.0）
   - リリースノートを記載
   - ビルドしたバイナリをアップロード

## バイナリの配布

### ダウンロードリンク

リリース後、以下のURLで配布:
```
https://github.com/Nyayuta1060/Horloq/releases/latest/download/horloq-linux-x86_64
https://github.com/Nyayuta1060/Horloq/releases/latest/download/horloq-windows-x86_64.exe
https://github.com/Nyayuta1060/Horloq/releases/latest/download/horloq-macos-x86_64
```

### インストール方法（ユーザー向け）

#### Linux
```bash
# ダウンロード
wget https://github.com/Nyayuta1060/Horloq/releases/latest/download/horloq-linux-x86_64

# 実行権限を付与
chmod +x horloq-linux-x86_64

# 実行
./horloq-linux-x86_64

# オプション: /usr/local/binに移動
sudo mv horloq-linux-x86_64 /usr/local/bin/horloq
```

#### Windows
1. https://github.com/Nyayuta1060/Horloq/releases/latest からダウンロード
2. `horloq-windows-x86_64.exe` をダブルクリックして実行

#### macOS
```bash
# ダウンロード
curl -L -o horloq https://github.com/Nyayuta1060/Horloq/releases/latest/download/horloq-macos-x86_64

# 実行権限を付与
chmod +x horloq

# 初回実行時にセキュリティ警告が出る場合
xattr -d com.apple.quarantine horloq

# 実行
./horloq
```

## バージョン管理

### セマンティックバージョニング

- **MAJOR** (v1.0.0): 互換性のない変更
- **MINOR** (v0.1.0): 後方互換性のある機能追加
- **PATCH** (v0.0.1): 後方互換性のあるバグ修正

### バージョンの更新

1. `setup.py` の `version` を更新
2. `pyproject.toml` の `version` を更新（存在する場合）
3. `CHANGELOG.md` に変更点を記載
4. コミット＆タグ作成

```bash
git add setup.py CHANGELOG.md
git commit -m "chore: bump version to v0.1.0"
git tag v0.1.0
git push origin main --tags
```

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

### GitHub Actionsエラー

**問題**: アクションが失敗する

**解決**:
1. Actions タブでログを確認
2. requirements.txt に全ての依存関係が記載されているか確認
3. PyInstallerのバージョンを固定: `pip install pyinstaller==6.3.0`

## 参考リンク

- [PyInstaller Documentation](https://pyinstaller.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)
