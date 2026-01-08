#!/bin/bash
# ローカルビルドスクリプト

set -e

echo "🔨 Horloqをビルド中..."

# venv環境をアクティベート
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ venv環境をアクティベート"
fi

# PyInstallerがインストールされているか確認
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstallerをインストール中..."
    pip install pyinstaller
fi

# ビルド
echo "バイナリを作成中..."
pyinstaller build.spec

# 結果を表示
echo ""
echo "✅ ビルド完了！"
echo "バイナリファイル: dist/horloq"
echo ""
echo "実行方法:"
echo "  ./dist/horloq"
