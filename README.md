# Horloq - 拡張可能デスクトップ据え置き時計

> Horloq(オルロック)はPython + CustomTkinterで作られた、プラグインシステムを備えた高機能デスクトップ時計アプリケーションです。

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://github.com/Nyayuta1060/Horloq/workflows/Build%20and%20Release/badge.svg)](https://github.com/Nyayuta1060/Horloq/actions)

## ✨ 特徴

- 🕐 **デジタル/アナログ時計表示** - 自由に切り替え可能な時計表示
- 🎨 **カスタマイズ可能なテーマ** - 色、フォント、透明度など自由にカスタマイズ
- 🔌 **プラグインシステム** - 機能を自由に追加・拡張できる
- 🌤️ **標準プラグイン搭載** - 天気、カレンダー、タイマーなど
- 💻 **クロスプラットフォーム** - Windows, macOS, Linux対応
- 🪶 **軽量** - メモリ使用量100MB以下
- 🎯 **常に最前面表示** - 作業中も時計を確認できる

## 📸 スクリーンショット

<!-- TODO: スクリーンショットを追加 -->

## 🚀 クイックスタート

### インストール

#### 方法1: バイナリダウンロード（推奨）

[GitHub Releases](https://github.com/Nyayuta1060/Horloq/releases) から最新版をダウンロード：

- Windows: `Horloq-windows.exe`
- macOS: `Horloq-macos`
- Linux: `Horloq-linux`

#### 方法2: ソースからビルド

```bash
# リポジトリをクローン
git clone https://github.com/Nyayuta1060/Horloq.git
cd Horloq

# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 依存関係をインストール
pip install -r requirements.txt

# 実行
python -m horloq
```

> **注意**: 現在はアルファ版です。基本機能のみ実装されています。

### 基本的な使い方

1. **起動**: アプリケーションを起動すると、デスクトップに時計が表示されます
2. **設定**: 時計の設定は `~/.config/horloq/config.yaml` で管理されます
3. **ドラッグで移動**: 時計ウィンドウをドラッグして好きな位置に配置

## 📦 プラグイン

現在、サンプルプラグイン(hello)が実装されています。今後、以下のプラグインを追加予定:

| プラグイン | 説明 | ステータス |
|----------|------|----------|
| 🌤️ **天気** | 現在の天気と気温を表示 | 計画中 |
| 📅 **カレンダー** | 月表示カレンダーと祝日表示 | 計画中 |
| ⏱️ **タイマー** | カウントダウンタイマー | 計画中 |
| ⏲️ **ストップウォッチ** | 精密時間計測 | 計画中 |

## 🔧 開発

### 環境構築

```bash
# リポジトリをクローン
git clone https://github.com/Nyayuta1060/Horloq.git
cd Horloq

# 仮想環境を作成・有効化
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 開発用依存関係をインストール
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 開発モードで実行
python -m horloq
```

### プラグイン開発

独自のプラグインを作成する方法：

```python
# plugins/my-plugin/plugin.py
from horloq.plugins.base import PluginBase

class Plugin(PluginBase):
    def activate(self):
        print("My plugin activated!")
        # 初期化処理
    
    def deactivate(self):
        print("My plugin deactivated!")
        # クリーンアップ処理
```

詳細は [開発ガイド](docs/DEVELOPMENT.md) を参照してください。

### ビルド

```bash
# PyInstallerでビルド
pyinstaller horloq.spec

# ビルド結果
ls dist/
```

## 📚 ドキュメント

- [アーキテクチャ設計](docs/ARCHITECTURE.md) - システム全体の設計
- [機能仕様書](docs/FEATURES.md) - 全機能の詳細仕様
- [技術設計書](docs/TECHNICAL_DESIGN.md) - API設計とデータフロー
- [Python実装詳細](docs/PYTHON_IMPLEMENTATION.md) - コード実装の詳細
- [開発ガイド](docs/DEVELOPMENT.md) - 開発環境とコーディング規約

## 🤝 コントリビューション

コントリビューションを歓迎します！以下の手順でお願いします：

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'feat: add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - モダンなTkinter UI
- [PyInstaller](https://pyinstaller.org/) - Pythonアプリのパッケージング
- すべてのコントリビューターの皆様

## 📞 お問い合わせ

- GitHub Issues: [https://github.com/Nyayuta1060/Horloq/issues](https://github.com/Nyayuta1060/Horloq/issues)
- プロジェクトリンク: [https://github.com/Nyayuta1060/Horloq](https://github.com/Nyayuta1060/Horloq)

---

Made with ❤️ by Nyayuta1060