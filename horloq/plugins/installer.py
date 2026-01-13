"""
プラグインインストーラー
"""

import os
import sys
import shutil
import subprocess
import tempfile
import yaml
import urllib.request
from pathlib import Path
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse


class PluginInstaller:
    """プラグインのインストール・管理"""
    
    def __init__(self, plugin_dir: Path):
        """
        初期化
        
        Args:
            plugin_dir: プラグインディレクトリ
        """
        self.plugin_dir = plugin_dir
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
    
    def install_from_github(self, repo_url: str, subdir: str = None) -> tuple[bool, str]:
        """
        GitHubリポジトリからプラグインをインストール
        
        Args:
            repo_url: GitHubリポジトリURL (例: https://github.com/user/horloq-plugin-xxx)
                     または短縮形式 (例: user/horloq-plugin-xxx)
                     サブディレクトリ指定 (例: user/horloq-plugins:weather)
            subdir: サブディレクトリ（オプション）
        
        Returns:
            (成功フラグ, メッセージ)
        """
        try:
            # サブディレクトリ指定がある場合（username/repo:subdir形式）
            if ':' in repo_url and not repo_url.startswith('http'):
                repo_url, subdir = repo_url.split(':', 1)
            
            # URLの正規化
            if not repo_url.startswith("http"):
                repo_url = f"https://github.com/{repo_url}"
            
            # 一時ディレクトリにクローン
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)
                
                # git clone
                result = subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, str(tmp_path / "plugin")],
                    capture_output=True,
                    text=True,
                )
                
                if result.returncode != 0:
                    return False, f"クローンに失敗しました: {result.stderr}"
                
                plugin_path = tmp_path / "plugin"
                
                # サブディレクトリが指定されている場合
                if subdir:
                    plugin_path = plugin_path / subdir
                    if not plugin_path.exists():
                        return False, f"サブディレクトリ '{subdir}' が見つかりません"
                
                # plugin.yamlを読み込む
                metadata_path = plugin_path / "plugin.yaml"
                if not metadata_path.exists():
                    return False, "plugin.yamlが見つかりません"
                
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = yaml.safe_load(f)
                
                plugin_name = metadata.get("name")
                if not plugin_name:
                    return False, "plugin.yamlにnameが指定されていません"
                
                # インストール先
                install_path = self.plugin_dir / plugin_name
                
                # 既存のプラグインを確認
                if install_path.exists():
                    return False, f"プラグイン '{plugin_name}' は既にインストールされています"
                
                # プラグインをコピー
                shutil.copytree(plugin_path, install_path, dirs_exist_ok=True)
                
                # .gitディレクトリを削除
                git_dir = install_path / ".git"
                if git_dir.exists():
                    shutil.rmtree(git_dir)
                
                # 依存関係をインストール
                requirements_path = install_path / "requirements.txt"
                dep_message = ""
                if requirements_path.exists():
                    success, message = self._install_dependencies(requirements_path)
                    if not success:
                        # 依存関係のインストールに失敗してもプラグイン自体はインストール
                        dep_message = f"\n警告: {message}"
                    else:
                        dep_message = f"\n{message}"
                
                version = metadata.get("version", "不明")
                return True, f"プラグイン '{plugin_name}' (v{version}) をインストールしました{dep_message}"
        
        except Exception as e:
            return False, f"エラー: {str(e)}"
    
    def install_from_local(self, plugin_path: Path) -> tuple[bool, str]:
        """
        ローカルディレクトリからプラグインをインストール
        
        Args:
            plugin_path: プラグインディレクトリのパス
        
        Returns:
            (成功フラグ, メッセージ)
        """
        try:
            # plugin.yamlを読み込む
            metadata_path = plugin_path / "plugin.yaml"
            if not metadata_path.exists():
                return False, "plugin.yamlが見つかりません"
            
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = yaml.safe_load(f)
            
            plugin_name = metadata.get("name")
            if not plugin_name:
                return False, "plugin.yamlにnameが指定されていません"
            
            # インストール先
            install_path = self.plugin_dir / plugin_name
            
            # 既存のプラグインを確認
            if install_path.exists():
                return False, f"プラグイン '{plugin_name}' は既にインストールされています"
            
            # プラグインをコピー
            shutil.copytree(plugin_path, install_path, dirs_exist_ok=True)
            
            # 依存関係をインストール
            requirements_path = install_path / "requirements.txt"
            dep_message = ""
            if requirements_path.exists():
                success, message = self._install_dependencies(requirements_path)
                if not success:
                    # 依存関係のインストールに失敗してもプラグイン自体はインストール
                    dep_message = f"\n警告: {message}"
                else:
                    dep_message = f"\n{message}"
            
            version = metadata.get("version", "不明")
            return True, f"プラグイン '{plugin_name}' (v{version}) をインストールしました{dep_message}"
        
        except Exception as e:
            return False, f"エラー: {str(e)}"
    
    def uninstall(self, plugin_name: str) -> tuple[bool, str]:
        """
        プラグインをアンインストール
        
        Args:
            plugin_name: プラグイン名
        
        Returns:
            (成功フラグ, メッセージ)
        """
        try:
            plugin_path = self.plugin_dir / plugin_name
            
            if not plugin_path.exists():
                return False, f"プラグイン '{plugin_name}' が見つかりません"
            
            # ディレクトリを削除
            shutil.rmtree(plugin_path)
            
            return True, f"プラグイン '{plugin_name}' をアンインストールしました"
        
        except Exception as e:
            return False, f"エラー: {str(e)}"
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        プラグイン情報を取得
        
        Args:
            plugin_name: プラグイン名
        
        Returns:
            プラグイン情報（存在しない場合はNone）
        """
        try:
            plugin_path = self.plugin_dir / plugin_name
            metadata_path = plugin_path / "plugin.yaml"
            
            if not metadata_path.exists():
                return None
            
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = yaml.safe_load(f)
            
            return metadata
        
        except Exception:
            return None
    
    def list_installed_plugins(self) -> list[Dict[str, Any]]:
        """
        インストール済みプラグインの一覧を取得
        
        Returns:
            プラグイン情報のリスト
        """
        plugins = []
        
        if not self.plugin_dir.exists():
            return plugins
        
        for item in self.plugin_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                info = self.get_plugin_info(item.name)
                if info:
                    info["directory"] = item.name
                    plugins.append(info)
        
        return plugins
    
    def fetch_plugin_catalog(self, repo_url: str) -> tuple[bool, Optional[List[Dict[str, Any]]]]:
        """
        リポジトリからプラグインカタログを取得
        
        Args:
            repo_url: GitHubリポジトリURL (例: user/horloq-plugins)
        
        Returns:
            (成功フラグ, プラグイン一覧)
        """
        try:
            # URLの正規化
            if not repo_url.startswith("http"):
                # user/repo 形式の場合
                parts = repo_url.split('/')
                if len(parts) == 2:
                    user, repo = parts
                    catalog_url = f"https://raw.githubusercontent.com/{user}/{repo}/main/plugins.yaml"
                else:
                    return False, None
            else:
                return False, None
            
            # カタログをダウンロード
            with urllib.request.urlopen(catalog_url) as response:
                catalog_data = yaml.safe_load(response.read())
            
            if not catalog_data or 'plugins' not in catalog_data:
                return False, None
            
            # リポジトリ情報を各プラグインに追加
            repo = catalog_data.get('repository', repo_url)
            plugins = []
            for plugin in catalog_data['plugins']:
                plugin['repository'] = repo
                plugins.append(plugin)
            
            return True, plugins
        
        except Exception as e:
            return False, None
    
    def _install_dependencies(self, requirements_path: Path) -> tuple[bool, str]:
        """
        依存関係をインストール
        
        Args:
            requirements_path: requirements.txtのパス
        
        Returns:
            (成功フラグ, メッセージ)
        """
        try:
            # Python実行可能ファイルのパスを取得
            python_exe = sys.executable
            
            # PyInstallerバイナリの場合、システムのPythonを探す
            if getattr(sys, 'frozen', False):
                # Windowsの場合
                if sys.platform == 'win32':
                    # py launcherを試す
                    try:
                        subprocess.run(['py', '--version'], capture_output=True, check=True)
                        python_exe = 'py'
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        # python3を試す
                        try:
                            subprocess.run(['python3', '--version'], capture_output=True, check=True)
                            python_exe = 'python3'
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            # pythonを試す
                            try:
                                subprocess.run(['python', '--version'], capture_output=True, check=True)
                                python_exe = 'python'
                            except (subprocess.CalledProcessError, FileNotFoundError):
                                return False, (
                                    "Pythonが見つかりません。\n"
                                    "依存関係を手動でインストールしてください:\n"
                                    f"python -m pip install -r {requirements_path.name}"
                                )
                else:
                    # Linux/macOSの場合
                    python_exe = 'python3'
            
            # パッケージリストを読み込み
            installed_packages = []
            with open(requirements_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        pkg = line.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].strip()
                        if pkg:
                            installed_packages.append(pkg)
            
            if not installed_packages:
                return True, "インストールする依存関係がありません"
            
            # Windowsでの特別な処理
            extra_args = []
            if sys.platform == 'win32':
                # --user オプションで権限エラーを回避
                extra_args.append('--user')
            
            # pipコマンドを構築
            pip_cmd = [python_exe, "-m", "pip", "install", "-r", str(requirements_path)]
            pip_cmd.extend(extra_args)
            
            # 環境変数を設定（文字エンコーディング問題を回避）
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            # Windowsでshell=Trueを使う場合はコマンドを文字列に変換
            if sys.platform == 'win32':
                # コマンドを文字列に変換（引用符でパスを保護）
                pip_cmd_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in pip_cmd)
                result = subprocess.run(
                    pip_cmd_str,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    env=env,
                    shell=True,
                )
            else:
                # Linux/macOSではリストのまま実行
                result = subprocess.run(
                    pip_cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    env=env,
                    shell=False,
                )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "不明なエラー"
                
                # Windowsで権限エラーの場合は管理者権限の案内
                if sys.platform == 'win32' and ('permission' in error_msg.lower() or 'access' in error_msg.lower()):
                    return False, (
                        "依存関係のインストールに失敗しました（権限エラー）。\n\n"
                        "以下の方法をお試しください：\n"
                        "1. コマンドプロンプトを管理者として実行し、以下を実行:\n"
                        f"   python -m pip install -r {requirements_path}\n\n"
                        "2. または手動でパッケージをインストール:\n"
                        f"   python -m pip install {' '.join(installed_packages)}\n\n"
                        f"詳細: {error_msg}"
                    )
                
                return False, (
                    "依存関係のインストールに失敗しました。\n\n"
                    "手動でインストールしてください:\n"
                    f"python -m pip install -r {requirements_path.name}\n\n"
                    f"詳細: {error_msg}"
                )
            
            pkg_list = ', '.join(installed_packages)
            return True, f"依存関係をインストールしました: {pkg_list}"
        
        except subprocess.TimeoutExpired:
            return False, "依存関係のインストールがタイムアウトしました。\nネットワーク接続を確認してください。"
        except Exception as e:
            return False, f"依存関係のインストール中にエラーが発生しました: {str(e)}"
    
    def check_for_updates(self, repo_url: str = "Nyayuta1060/Horloq-Plugins") -> tuple[bool, List[Dict[str, Any]]]:
        """
        インストール済みプラグインの更新をチェック
        
        Args:
            repo_url: プラグインリポジトリURL
        
        Returns:
            (成功フラグ, 更新可能なプラグインのリスト)
            各プラグイン情報は以下を含む:
            - name: プラグイン名
            - current_version: 現在のバージョン
            - latest_version: 最新バージョン
            - description: プラグインの説明
        """
        try:
            # インストール済みプラグイン一覧を取得
            installed = self.list_installed_plugins()
            if not installed:
                return True, []
            
            # リモートカタログを取得
            success, remote_plugins = self.fetch_plugin_catalog(repo_url)
            if not success or not remote_plugins:
                return False, []
            
            # リモートプラグインを辞書化（高速検索用）
            remote_dict = {p['name']: p for p in remote_plugins}
            
            # 更新可能なプラグインをチェック
            updates_available = []
            for local_plugin in installed:
                plugin_name = local_plugin.get('name')
                local_version = local_plugin.get('version', '0.0.0')
                
                # リモートに同じプラグインがあるかチェック
                if plugin_name in remote_dict:
                    remote_version = remote_dict[plugin_name].get('version', '0.0.0')
                    
                    # バージョン比較
                    if self._is_newer_version(remote_version, local_version):
                        updates_available.append({
                            'name': plugin_name,
                            'current_version': local_version,
                            'latest_version': remote_version,
                            'description': remote_dict[plugin_name].get('description', ''),
                            'repository': repo_url
                        })
            
            return True, updates_available
        
        except Exception as e:
            return False, []
    
    def _is_newer_version(self, version1: str, version2: str) -> bool:
        """
        version1がversion2より新しいかチェック（簡易セマンティックバージョニング）
        
        Args:
            version1: 比較するバージョン（新しいと思われる方）
            version2: 比較するバージョン（古いと思われる方）
        
        Returns:
            version1がversion2より新しい場合True
        """
        try:
            # バージョン文字列を数値リストに変換
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # 長さを揃える（短い方に0を追加）
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            # 各パートを比較
            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return True
                elif v1_parts[i] < v2_parts[i]:
                    return False
            
            # 完全に同じ
            return False
        
        except (ValueError, AttributeError):
            # パースエラーの場合は文字列比較
            return version1 > version2

