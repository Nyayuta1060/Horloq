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
2. **右クリックメニュー**: 時計を右クリックして設定やプラグイン管理にアクセス
   - ⚙️ 設定：時計の表示設定やテーマを変更
   - 🔌 プラグイン管理：プラグインの有効/無効を切り替え
   - ❌ 終了：アプリケーションを終了
3. **設定**: 時計の設定は `~/.config/horloq/config.yaml` で管理されます
4. **ドラッグで移動**: 時計ウィンドウをドラッグして好きな位置に配置

## 📦 プラグイン

Horloqはプラグインシステムにより機能を拡張できます。すべてのプラグインはユーザーが必要に応じてインストールできます。

### 公式プラグイン

| プラグイン             | 説明                                         |
| ---------------------- | -------------------------------------------- |
| 👋 **Hello**            | サンプルプラグイン                           |
| ⏱️ **タイマー**         | カウントダウンタイマー（プリセット機能付き） |
| ⏲️ **ストップウォッチ** | 精密時間計測（ラップタイム機能付き）         |

公式プラグインは別リポジトリで管理されています。詳細は [公式プラグイン集](https://github.com/Nyayuta1060/horloq-official-plugins)（準備中）を参照してください。

### プラグインの管理

#### GUIから

1. 右クリックメニューから「プラグイン管理」を選択
2. **公式プラグインをインストール:**
   - 「カタログから選択」をクリック
   - `Nyayuta1060/horloq-official-plugins`を入力（準備中）
   - 一覧から必要なプラグインを選択してインストール
3. **サードパーティプラグインをインストール:**
   - 「GitHubからインストール」- 単一プラグインをURLから直接インストール
   - 「カタログから選択」- モノレポのプラグイン一覧から選択してインストール

#### CLIから

```bash
# 公式プラグインをインストール（準備中）
python -m horloq plugin install Nyayuta1060/horloq-official-plugins:hello
python -m horloq plugin install Nyayuta1060/horloq-official-plugins:timer

# サードパーティプラグインをインストール
python -m horloq plugin install username/horloq-plugin-example

# モノレポから特定のプラグインをインストール
python -m horloq plugin install username/horloq-plugins:weather

# プラグインをアンインストール
python -m horloq plugin uninstall hello

# インストール済みプラグイン一覧
python -m horloq plugin list
```

### プラグイン開発

独自のプラグインを作成・配布できます。詳細は [プラグイン開発ガイド](docs/PLUGIN_DEVELOPMENT.md) を参照してください。
公式プラグインのサンプルコードは [サンプルプラグイン集](docs/EXAMPLE_PLUGINS.md) で確認できます。
#### 簡単な例

1. GitHubでリポジトリ作成（例: `horloq-plugin-myfeature`）
2. プラグインファイルを作成：

```
horloq-plugin-myfeature/
├── plugin.yaml       # メタデータ
├── __init__.py      # プラグイン本体
└── README.md
```

3. ユーザーはこうインストール：

```bash
python -m horloq plugin install yourusername/horloq-plugin-myfeature
```

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
# __init__.py
from horloq.plugins.base import PluginBase
import customtkinter as ctk

class MyPlugin(PluginBase):
    def __init__(self, app_context):
        super().__init__(
            name="my_plugin",
            version="1.0.0",
            author="Your Name",
            description="My awesome plugin",
            app_context=app_context,
        )
    
    def initialize(self):
        return True
    
    def create_widget(self, parent):
        frame = ctk.CTkFrame(parent)
        label = ctk.CTkLabel(frame, text="Hello from my plugin!")
        label.pack(pady=10)
        return frame

# プラグインクラスをエクスポート
Plugin = MyPlugin
```

詳細は [プラグイン開発ガイド](docs/PLUGIN_DEVELOPMENT.md) を参照してください。

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