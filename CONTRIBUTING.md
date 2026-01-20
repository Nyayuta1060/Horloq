# コントリビューションガイド

Horloqプロジェクトへの貢献に興味を持っていただき、ありがとうございます！
このガイドでは、プロジェクトへの貢献方法を説明します。

## 📋 目次

- [行動規範](#行動規範)
- [始め方](#始め方)
- [開発の流れ](#開発の流れ)
- [コーディング規約](#コーディング規約)
- [コミットメッセージ規約](#コミットメッセージ規約)
- [プルリクエストの作成](#プルリクエストの作成)
- [プラグイン開発](#プラグイン開発)

## 行動規範

このプロジェクトでは、すべての参加者に敬意を持って接することを期待しています。
建設的で前向きな環境を維持するため、以下を心がけてください：

- 他の貢献者を尊重する
- 建設的なフィードバックを提供する
- 異なる視点や経験を受け入れる
- プロジェクトとコミュニティに焦点を当てる

## 始め方

### 1. リポジトリをフォーク

GitHubでリポジトリをフォークし、ローカルにクローンします：

```bash
git clone https://github.com/YOUR_USERNAME/Horloq.git
cd Horloq
```

### 2. 開発環境をセットアップ

```bash
# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 依存関係をインストール
pip install -e .
pip install pytest ruff black mypy pylint
```

### 3. リモートリポジトリを追加

```bash
git remote add upstream https://github.com/Nyayuta1060/Horloq.git
```

## 開発の流れ

### 1. ブランチを作成

機能追加やバグ修正ごとに新しいブランチを作成してください：

```bash
git checkout -b feature/amazing-feature
# または
git checkout -b fix/bug-description
```

ブランチ名の規則：
- `feature/` - 新機能
- `fix/` - バグ修正
- `docs/` - ドキュメントのみの変更
- `refactor/` - リファクタリング
- `test/` - テストの追加・修正

### 2. 変更を実装

コードを書く際は以下を確認してください：

- コードが動作することを確認
- 適切なコメントを追加
- 新機能にはテストを追加
- ドキュメントを更新（必要な場合）

### 3. コードをテスト

```bash
# テストを実行
pytest

# コードスタイルをチェック
ruff check horloq/
black --check horloq/

# 型チェック
mypy horloq/
```

### 4. 変更をコミット

こまめにコミットを作成してください：

```bash
git add .
git commit -m "feat: 素晴らしい機能を追加"
```

## コーディング規約

### Python スタイル

- **PEP 8** に従う
- **型ヒント** を使用（Python 3.11+）
- **Docstring** は必須（関数、クラス、モジュール）
- **行の長さ**: 100文字まで

```python
def example_function(param: str, count: int = 0) -> bool:
    """
    関数の説明
    
    Args:
        param: パラメータの説明
        count: カウントの説明
        
    Returns:
        成功時True
    """
    return True
```

### ファイル構成

```
horloq/
├── core/          # コア機能
├── ui/            # UIコンポーネント
├── plugins/       # プラグインシステム
└── utils/         # ユーティリティ
```

### インポート順序

1. 標準ライブラリ
2. サードパーティライブラリ
3. ローカルモジュール

```python
import os
from pathlib import Path

import customtkinter as ctk
from typing import Optional

from horloq.core import ConfigManager
```

## コミットメッセージ規約

[Conventional Commits](https://www.conventionalcommits.org/) 形式を使用：

```
<type>: <subject>

<body>

<footer>
```

### Type の種類

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマットなど）
- `refactor`: バグ修正でも機能追加でもないコード変更
- `perf`: パフォーマンス向上
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更

### 例

```bash
feat: デジタル時計にアニメーション効果を追加

秒の表示にフェードイン効果を追加しました。
設定画面でアニメーションのオン/オフを切り替えられます。

Closes #123
```

## プルリクエストの作成

### 1. 変更をプッシュ

```bash
git push origin feature/amazing-feature
```

### 2. プルリクエストを開く

GitHub上でプルリクエストを作成し、以下を記載してください：

- **タイトル**: 変更内容を簡潔に説明
- **説明**: 
  - 何を変更したか
  - なぜ変更したか
  - どのようにテストしたか
- **関連Issue**: `Closes #123` などで参照

### プルリクエストのチェックリスト

- [ ] コードが動作することを確認
- [ ] テストが通ることを確認
- [ ] コーディング規約に従っている
- [ ] ドキュメントを更新（必要な場合）
- [ ] コミットメッセージが規約に従っている
- [ ] 変更が1つの機能/修正に集中している

## プラグイン開発

プラグインを開発する場合は、以下のガイドラインに従ってください：

### plugin.yaml の作成

プラグインのメタデータは `plugin.yaml` で管理します：

```yaml
name: my-plugin
version: 1.0.0
author: Your Name
description: プラグインの説明
min_horloq_version: 0.1.0
```

### プラグインクラスの実装

```python
from horloq.plugins.base import PluginBase
import customtkinter as ctk

class MyPlugin(PluginBase):
    """プラグインの説明"""
    
    def __init__(self, app_context):
        # plugin.yamlから自動的にメタデータを読み込みます
        super().__init__(app_context)
    
    def initialize(self) -> bool:
        """初期化処理"""
        return True
    
    def shutdown(self):
        """終了処理"""
        pass
    
    def create_widget(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """UIウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        # ウィジェットを追加
        return frame

# プラグインクラスをエクスポート
Plugin = MyPlugin
```

**重要**: 
- `plugin.yaml` がメタデータの唯一の情報源（Single Source of Truth）
- `__init__` では `super().__init__(app_context)` のみ呼び出す
- `name`、`version`、`author`、`description` は自動読み込み
- Python コード内でのハードコーディングは不要

詳細は以下のドキュメントを参照してください：
- [プラグイン開発ガイド](docs/PLUGIN_DEVELOPMENT.md)
- [サンプルプラグイン集](docs/EXAMPLE_PLUGINS.md)
- [開発者ドキュメント](docs/DEVELOPMENT.md)

## 質問やヘルプ

質問がある場合は、以下の方法でお気軽にお問い合わせください：

- **GitHub Issues**: バグ報告や機能リクエスト
- **GitHub Discussions**: 一般的な質問やアイデアの共有

## ライセンス

コントリビューションを行うことで、あなたの貢献がプロジェクトのライセンス（MIT License）の下で公開されることに同意したものとみなされます。

---

再度、Horloqプロジェクトへの貢献に感謝します！
