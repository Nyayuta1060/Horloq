"""
CLI コマンド
"""

import sys
import argparse
from pathlib import Path
from .core.config import ConfigManager
from .plugins.installer import PluginInstaller


def plugin_command(args):
    """プラグイン管理コマンド"""
    config = ConfigManager()
    plugin_dir = config.config_path.parent / "plugins"
    installer = PluginInstaller(plugin_dir)
    
    if args.plugin_action == "install":
        if not args.source:
            print("エラー: インストール元を指定してください")
            print("例: horloq plugin install username/repo-name")
            return 1
        
        print(f"プラグインをインストールしています: {args.source}")
        success, message = installer.install_from_github(args.source)
        print(message)
        return 0 if success else 1
    
    elif args.plugin_action == "uninstall":
        if not args.source:
            print("エラー: プラグイン名を指定してください")
            print("例: horloq plugin uninstall plugin-name")
            return 1
        
        print(f"プラグインをアンインストールしています: {args.source}")
        success, message = installer.uninstall(args.source)
        print(message)
        return 0 if success else 1
    
    elif args.plugin_action == "list":
        plugins = installer.list_installed_plugins()
        if not plugins:
            print("インストール済みのプラグインはありません")
        else:
            print("インストール済みプラグイン:")
            print("-" * 60)
            for plugin in plugins:
                name = plugin.get("name", "不明")
                version = plugin.get("version", "不明")
                author = plugin.get("author", "不明")
                desc = plugin.get("description", "説明なし")
                print(f"  {name} (v{version}) by {author}")
                print(f"    {desc}")
                print()
        return 0
    
    else:
        print("エラー: 不明なアクション")
        return 1


def main():
    """CLIメイン関数"""
    parser = argparse.ArgumentParser(
        prog="horloq",
        description="Horloq - 拡張可能デスクトップ据え置き時計",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="コマンド")
    
    # pluginコマンド
    plugin_parser = subparsers.add_parser("plugin", help="プラグイン管理")
    plugin_parser.add_argument(
        "plugin_action",
        choices=["install", "uninstall", "list"],
        help="アクション",
    )
    plugin_parser.add_argument(
        "source",
        nargs="?",
        help="インストール元（GitHubリポジトリまたはプラグイン名）",
    )
    
    args = parser.parse_args()
    
    if args.command == "plugin":
        return plugin_command(args)
    elif args.command is None:
        # コマンドなしの場合はGUIを起動
        from .core.app import HorloqApp
        app = HorloqApp()
        app.run()
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
