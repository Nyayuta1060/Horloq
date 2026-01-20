"""
アップデートチェッカー
"""

import urllib.request
import json
from typing import Optional, Tuple
from .. import __version__


class UpdateChecker:
    """Horloq本体のアップデートチェック"""
    
    GITHUB_API_URL = "https://api.github.com/repos/Nyayuta1060/Horloq/releases/latest"
    
    def __init__(self):
        self.current_version = __version__
        self.latest_version = None
        self.latest_assets = []
    
    def check_for_updates(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        最新バージョンをチェック
        
        Returns:
            (更新があるか, 最新バージョン, リリースURL)
        """
        try:
            # GitHub APIから最新リリース情報を取得
            req = urllib.request.Request(
                self.GITHUB_API_URL,
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            latest_version = data.get('tag_name', '').lstrip('v')
            release_url = data.get('html_url', '')
            release_notes = data.get('body', '')
            
            # アセット情報を保存
            self.latest_version = latest_version
            self.latest_assets = data.get('assets', [])
            
            if not latest_version:
                return False, None, None
            
            # バージョン比較
            if self._is_newer_version(latest_version, self.current_version):
                return True, latest_version, release_url
            
            return False, latest_version, release_url
        
        except Exception as e:
            # ネットワークエラーなどは無視（サイレントに失敗）
            print(f"[UpdateChecker] アップデートチェックに失敗: {e}")
            return False, None, None
    
    def _is_newer_version(self, latest: str, current: str) -> bool:
        """
        バージョン比較（セマンティックバージョニング）
        
        Args:
            latest: 最新バージョン（例: "0.2.1"）
            current: 現在のバージョン（例: "0.2.0"）
        
        Returns:
            最新バージョンの方が新しい場合True
        """
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # 不足している部分を0で埋める
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return latest_parts > current_parts
        
        except (ValueError, AttributeError):
            return False
    
    def get_current_version(self) -> str:
        """現在のバージョンを取得"""
        return self.current_version
    
    def get_download_url(self, platform: str = None) -> str:
        """
        ダウンロードURLを取得
        
        Args:
            platform: プラットフォーム ('windows', 'linux', 'macos')
        
        Returns:
            ダウンロードURL
        """
        # 最新バージョンが設定されている場合は、そのバージョンを使用
        version = self.latest_version if self.latest_version else self.current_version
        base_url = f"https://github.com/Nyayuta1060/Horloq/releases/latest/download/"
        
        if platform == 'windows':
            return f"{base_url}horloq-windows-x86_64-{version}.exe"
        elif platform == 'linux':
            return f"{base_url}horloq-linux-x86_64-{version}"
        elif platform == 'macos':
            return f"{base_url}horloq-macos-x86_64-{version}"
        else:
            return "https://github.com/Nyayuta1060/Horloq/releases/latest"
