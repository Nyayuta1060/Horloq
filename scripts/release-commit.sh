#!/bin/bash

set -e

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${GREEN}Horloq Release Commit Script${NC}"
echo "=================================="

# バージョン番号の入力
read -p "Enter version tag (e.g., v0.3.0): " VERSION

# バージョン形式のチェック
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Error: Invalid version format. Use format: v0.3.0${NC}"
    exit 1
fi

# v を除いたバージョン番号
VERSION_NUMBER="${VERSION#v}"

# horloq/__init__.py からバージョンを取得
INIT_FILE="$PROJECT_ROOT/horloq/__init__.py"
if [ ! -f "$INIT_FILE" ]; then
    echo -e "${RED}Error: $INIT_FILE not found${NC}"
    exit 1
fi

CURRENT_VERSION=$(grep -oP '__version__\s*=\s*"\K[^"]+' "$INIT_FILE")

# バージョンの整合性確認
echo ""
echo "Version in __init__.py: $CURRENT_VERSION"
echo "Requested tag version:  $VERSION_NUMBER"
echo ""

if [ "$CURRENT_VERSION" != "$VERSION_NUMBER" ]; then
    echo -e "${YELLOW}Warning: Version mismatch!${NC}"
    echo "The version in __init__.py ($CURRENT_VERSION) does not match the tag ($VERSION_NUMBER)"
    read -p "Do you want to update __init__.py to $VERSION_NUMBER? (y/n): " UPDATE_INIT
    
    if [ "$UPDATE_INIT" = "y" ] || [ "$UPDATE_INIT" = "Y" ]; then
        # __init__.py を更新
        sed -i "s/__version__ = \".*\"/__version__ = \"$VERSION_NUMBER\"/" "$INIT_FILE"
        echo -e "${GREEN}✓ Updated __init__.py to version $VERSION_NUMBER${NC}"
    else
        echo -e "${RED}Aborted. Please update __init__.py manually.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Version matches!${NC}"
fi

# 確認
echo ""
echo "The following operations will be performed:"
echo "  1. git add horloq/__init__.py"
echo "  2. git commit -m \"chore: bump version to $VERSION_NUMBER\""
echo "  3. git tag $VERSION"
echo "  4. git push origin main --tags"
echo ""
read -p "Continue? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo -e "${YELLOW}Aborted.${NC}"
    exit 0
fi

# Git 操作の実行
echo ""
echo "Executing git operations..."

cd "$PROJECT_ROOT"

# git add
git add horloq/__init__.py
echo -e "${GREEN}✓ git add horloq/__init__.py${NC}"

# git commit
git commit -m "chore: bump version to $VERSION_NUMBER"
echo -e "${GREEN}✓ git commit${NC}"

# git tag
git tag "$VERSION"
echo -e "${GREEN}✓ git tag $VERSION${NC}"

# git push
git push origin main --tags
echo -e "${GREEN}✓ git push origin main --tags${NC}"

echo ""
echo -e "${GREEN}Success! Version $VERSION has been released.${NC}"
echo ""
echo "Next steps:"
echo "  1. Wait for GitHub Actions to build binaries"
echo "  2. Go to https://github.com/Nyayuta1060/Horloq/releases"
echo "  3. Edit the draft release and add release notes"
echo "  4. Click 'Publish release'"
echo ""
