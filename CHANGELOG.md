# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-01-07

### Added
- 🎨 8つのエンジニア向けテーマ（VS Code Dark、GitHub Dark、Monokai Pro、One Dark、Nord、Dracula、Light、Dark）
- ⚙️ 設定画面（General、Clock、Theme、Window タブ）
- 🎨 テーマプレビュー機能
- 🔌 プラグインシステム
  - プラグインマネージャーUI
  - GitHubからのプラグインインストール
  - プラグインカタログブラウザ
  - 公式プラグインワンクリックアクセス
  - インストール済みプラグイン判定機能
- 🏆 公式プラグインリポジトリ対応
  - Hello プラグイン（サンプル）
  - Timer プラグイン（カウントダウン）
  - Stopwatch プラグイン（ストップウォッチ）
- 📝 コンテキストメニュー（右クリック）
- 🖥️ CLIコマンド（plugin install/uninstall/list）
- 📚 包括的なドキュメント
  - プラグイン開発ガイド
  - サンプルプラグイン集
  - アーキテクチャドキュメント

### Changed
- デフォルトテーマを "dark" から "vscode_dark" に変更
- プラグインローダーをディレクトリ形式に対応
- ウィンドウサイズの最適化

### Fixed
- CTkToplevel の grab_set() タイミング問題を解決
- プラグイン再検出機能の実装
- プラグイン情報表示の改善（plugin.yamlから直接読み込み）

### Removed
- ビルトインプラグイン（外部リポジトリに移行）

[0.1.0]: https://github.com/Nyayuta1060/Horloq/releases/tag/v0.1.0
