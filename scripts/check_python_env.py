# Windows環境でのパッケージパス確認スクリプト

import sys
import site
from pathlib import Path

print("=" * 60)
print("Python環境情報")
print("=" * 60)
print(f"Pythonバージョン: {sys.version}")
print(f"実行ファイル: {sys.executable}")
print(f"プラットフォーム: {sys.platform}")
print(f"Frozen: {getattr(sys, 'frozen', False)}")
print()

print("=" * 60)
print("site-packagesパス")
print("=" * 60)

# ユーザーsite-packages
user_site = site.getusersitepackages()
print(f"\nユーザーsite-packages: {user_site}")
if user_site:
    user_site_path = Path(user_site)
    if user_site_path.exists():
        print("  [OK] 存在します")
        print(f"  sys.pathに含まれる: {'[OK]' if user_site in sys.path else '[NG]'}")
        print("\n  インストール済みパッケージ (ディレクトリのみ):")
        try:
            for item in sorted(user_site_path.iterdir()):
                if item.is_dir() and not item.name.startswith('.') and not item.name.endswith('.dist-info'):
                    print(f"    - {item.name}")
        except Exception as e:
            print(f"    エラー: {e}")
    else:
        print("  [NG] 存在しません")

# ユーザーbase
user_base = site.getuserbase()
print(f"\nユーザーbase: {user_base}")
if user_base and sys.platform == 'win32':
    scripts_dir = Path(user_base) / "Scripts"
    print(f"\nScriptsディレクトリ: {scripts_dir}")
    if scripts_dir.exists():
        print("  [OK] 存在します")
        print(f"  sys.pathに含まれる: {'[OK]' if str(scripts_dir) in sys.path else '[NG]'}")
    else:
        print("  [NG] 存在しません")

# システムsite-packages
system_site = site.getsitepackages()
print(f"\nシステムsite-packages:")
for path in system_site:
    print(f"  - {path}")
    print(f"    sys.pathに含まれる: {'[OK]' if path in sys.path else '[NG]'}")

print()
print("=" * 60)
print("sys.path全体")
print("=" * 60)
for i, path in enumerate(sys.path, 1):
    print(f"{i:2d}. {path}")

print()
print("=" * 60)
print("特定パッケージの確認")
print("=" * 60)

packages_to_check = ['requests', 'pynput', 'pillow']
for package in packages_to_check:
    try:
        module = __import__(package)
        location = getattr(module, '__file__', 'N/A')
        print(f"[OK] {package}: {location}")
    except ImportError as e:
        print(f"[NG] {package}: インポートできません ({e})")

print()
print("=" * 60)
print("完了")
print("=" * 60)
