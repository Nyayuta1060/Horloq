# Horloq ドキュメントインデックス

> Horloqプロジェクトの全ドキュメントへのガイドです。  
> 目的に応じて適切なドキュメントをお選びください。

## 🗺️ ドキュメントマップ

```
docs/
├── README.md (このファイル)        - ドキュメント全体のナビゲーション
│
├── 📖 ユーザー向け
│   ├── FEATURES.md                 - 機能仕様書
│   └── WINDOWS_TROUBLESHOOTING.md  - Windows環境のトラブルシューティング
│
├── 🔌 プラグイン開発者向け
│   ├── PLUGIN_DEVELOPMENT.md       - プラグイン開発ガイド
│   └── EXAMPLE_PLUGINS.md          - サンプルプラグイン集
│
├── 👨‍💻 コントリビューター向け
│   ├── DEVELOPMENT.md              - 開発環境セットアップ
│   ├── ARCHITECTURE.md             - システムアーキテクチャ
│   ├── PYTHON_IMPLEMENTATION.md    - Python実装詳細
│   └── VERSION_MANAGEMENT.md       - バージョン管理 & リリース手順
│
└── 📋 その他
    └── assets/                     - 画像・リソースファイル
```

## 🎯 目的別ガイド

### 初めて使う方

1. **[README.md](../README.md)** - プロジェクト概要とクイックスタート
2. **[FEATURES.md](FEATURES.md)** - 利用可能な機能の一覧

### プラグインを作りたい方

1. **[PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md)** - プラグイン開発の完全ガイド
   - プラグイン構造
   - plugin.yamlの書き方
   - PluginBaseクラスの使い方
   - ベストプラクティス

2. **[EXAMPLE_PLUGINS.md](EXAMPLE_PLUGINS.md)** - 実装例
   - Hello プラグイン（基本）
   - Timer プラグイン（状態管理）
   - Stopwatch プラグイン（リアルタイム更新）

### Horloqの開発に貢献したい方

1. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - コントリビューションガイド
2. **[DEVELOPMENT.md](DEVELOPMENT.md)** - 開発環境のセットアップ
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - システム設計の理解
4. **[VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md)** - リリース手順

### 技術詳細を知りたい方

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - システム全体の設計思想
- **[PYTHON_IMPLEMENTATION.md](PYTHON_IMPLEMENTATION.md)** - Pythonコードの実装詳細

### 問題が発生した方

- **[WINDOWS_TROUBLESHOOTING.md](WINDOWS_TROUBLESHOOTING.md)** - Windows固有の問題
- **[GitHub Issues](https://github.com/Nyayuta1060/Horloq/issues)** - その他の問題

## 📚 ドキュメント詳細

### ユーザー向けドキュメント

#### [FEATURES.md](FEATURES.md)
**対象**: すべてのユーザー  
**内容**:
- コア機能（時計表示、テーマ、ウィンドウ管理）
- 設定管理
- プラグインシステムの概要
- 計画中の機能

**こんな時に読む**:
- Horloqでできることを知りたい
- 特定の機能の使い方を確認したい

#### [WINDOWS_TROUBLESHOOTING.md](WINDOWS_TROUBLESHOOTING.md)
**対象**: Windowsユーザー  
**内容**:
- プラグイン依存関係のインストールエラー
- 権限エラーの解決
- pynputビルドエラー
- Python PATHの設定

**こんな時に読む**:
- Windowsでエラーが発生した
- プラグインがインストールできない

### プラグイン開発者向けドキュメント

#### [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md)
**対象**: プラグイン作成者  
**内容**:
- プラグインの基本構造
- `plugin.yaml` の仕様（Single Source of Truth）
- `PluginBase` クラスの使い方
- プラグインライフサイクル
- 公開・配布方法

**こんな時に読む**:
- 初めてプラグインを作る
- plugin.yamlの書き方を確認したい
- プラグインを公開したい

#### [EXAMPLE_PLUGINS.md](EXAMPLE_PLUGINS.md)
**対象**: プラグイン開発者  
**内容**:
- Hello プラグイン - 最小構成
- Timer プラグイン - 状態管理とUI
- Stopwatch プラグイン - リアルタイム更新

**こんな時に読む**:
- 実装例を参考にしたい
- ベストプラクティスを知りたい

### コントリビューター向けドキュメント

#### [DEVELOPMENT.md](DEVELOPMENT.md)
**対象**: Horloq本体の開発者  
**内容**:
- 開発環境のセットアップ
- プロジェクト構造
- コーディング規約
- テスト実行
- デバッグ方法

**こんな時に読む**:
- Horloqの開発を始める
- コーディング規約を確認したい

#### [ARCHITECTURE.md](ARCHITECTURE.md)
**対象**: Horloq本体の開発者・アーキテクト  
**内容**:
- システム全体の設計
- 技術スタック
- コアコンポーネント
- プラグインシステム設計
- イベントシステム
- セキュリティ考慮事項

**こんな時に読む**:
- システム全体を理解したい
- 新機能の設計を検討している
- アーキテクチャ変更を提案したい

#### [PYTHON_IMPLEMENTATION.md](PYTHON_IMPLEMENTATION.md)
**対象**: Horloq本体の開発者  
**内容**:
- Pythonコードの詳細実装
- 設定管理システム
- プラグインシステムの実装
- UIコンポーネント設計

**こんな時に読む**:
- 具体的なコード実装を理解したい
- 既存コードを修正・拡張したい

#### [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md)
**対象**: メンテナー・リリース担当者  
**内容**:
- Single Source of Truth（`horloq/__init__.py`）
- バージョン更新手順
- ビルド方法
- GitHub Releasesでのリリース手順
- トラブルシューティング

**こんな時に読む**:
- 新バージョンをリリースする
- バージョン管理の仕組みを理解したい

## 📝 ドキュメント編集方針

### 原則

1. **明確さ** - 専門用語を避け、分かりやすく説明
2. **完全性** - 必要な情報をすべて含む
3. **最新性** - コードと同期を保つ
4. **簡潔さ** - 冗長な説明を避ける

### ドキュメントの種類

| 種類               | 対象読者       | 目的       | 例                       |
| ------------------ | -------------- | ---------- | ------------------------ |
| **ガイド**         | 初心者〜中級者 | 手順の説明 | PLUGIN_DEVELOPMENT.md    |
| **リファレンス**   | 開発者         | 技術詳細   | PYTHON_IMPLEMENTATION.md |
| **コンセプト**     | アーキテクト   | 設計思想   | ARCHITECTURE.md          |
| **チュートリアル** | 初心者         | 実践的学習 | EXAMPLE_PLUGINS.md       |

### 更新ルール

- コード変更に伴うドキュメント更新は同じPRに含める
- 古い情報は削除または更新（コメントアウトしない）
- 重複した情報は避け、相互リンクを活用

## 🔗 外部リソース

### 公式リンク
- [GitHub Repository](https://github.com/Nyayuta1060/Horloq)
- [Releases](https://github.com/Nyayuta1060/Horloq/releases)
- [Issues](https://github.com/Nyayuta1060/Horloq/issues)
- [公式プラグイン集](https://github.com/Nyayuta1060/Horloq-Plugins)

### 技術参考
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [Python Packaging Guide](https://packaging.python.org/)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [セマンティックバージョニング](https://semver.org/lang/ja/)

## 💡 ドキュメントへの貢献

ドキュメントの改善提案や誤字脱字の修正は歓迎します！

1. [Issues](https://github.com/Nyayuta1060/Horloq/issues) で報告
2. または直接 Pull Request を作成

---

**最終更新**: 2026年1月13日  
**メンテナー**: [@Nyayuta1060](https://github.com/Nyayuta1060)
