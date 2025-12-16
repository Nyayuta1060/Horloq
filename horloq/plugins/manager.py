"""
プラグインマネージャー
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from .base import PluginBase
from .loader import PluginLoader


class PluginManager:
    """プラグイン管理"""
    
    def __init__(self, app_context: Dict[str, Any], plugin_dirs: List[Path]):
        """
        初期化
        
        Args:
            app_context: アプリケーションコンテキスト
            plugin_dirs: プラグインディレクトリのリスト
        """
        self.app_context = app_context
        self.loader = PluginLoader(plugin_dirs)
        
        self._active_plugins: Dict[str, PluginBase] = {}
    
    def discover_plugins(self) -> List[str]:
        """
        利用可能なプラグインを検出
        
        Returns:
            プラグイン名のリスト
        """
        return self.loader.discover_plugins()
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        プラグインを読み込んで初期化
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            成功時True
        """
        # すでにアクティブの場合
        if plugin_name in self._active_plugins:
            return True
        
        # プラグインクラスを読み込む
        plugin_class = self.loader.load_plugin(plugin_name)
        if plugin_class is None:
            return False
        
        try:
            # プラグインインスタンスを作成
            plugin = plugin_class(self.app_context)
            
            # 初期化
            if not plugin.initialize():
                print(f"プラグインの初期化に失敗: {plugin_name}")
                return False
            
            # アクティブリストに追加
            self._active_plugins[plugin_name] = plugin
            plugin.enabled = True
            plugin.on_enable()
            
            return True
            
        except Exception as e:
            print(f"プラグインの読み込みエラー ({plugin_name}): {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        プラグインをアンロード
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            成功時True
        """
        if plugin_name not in self._active_plugins:
            return False
        
        try:
            plugin = self._active_plugins[plugin_name]
            
            # 無効化
            plugin.on_disable()
            plugin.enabled = False
            
            # 終了処理
            plugin.shutdown()
            
            # アクティブリストから削除
            del self._active_plugins[plugin_name]
            
            # ローダーからもアンロード
            self.loader.unload_plugin(plugin_name)
            
            return True
            
        except Exception as e:
            print(f"プラグインのアンロードエラー ({plugin_name}): {e}")
            return False
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginBase]:
        """
        プラグインインスタンスを取得
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            プラグインインスタンス（存在しない場合はNone）
        """
        return self._active_plugins.get(plugin_name)
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """
        プラグインを有効化
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            成功時True
        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            return self.load_plugin(plugin_name)
        
        if not plugin.enabled:
            plugin.enabled = True
            plugin.on_enable()
        
        return True
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """
        プラグインを無効化（アンロードはしない）
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            成功時True
        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            return False
        
        if plugin.enabled:
            plugin.on_disable()
            plugin.enabled = False
        
        return True
    
    def list_active_plugins(self) -> List[str]:
        """
        アクティブなプラグイン名のリストを取得
        
        Returns:
            プラグイン名のリスト
        """
        return list(self._active_plugins.keys())
    
    def list_enabled_plugins(self) -> List[str]:
        """
        有効なプラグイン名のリストを取得
        
        Returns:
            プラグイン名のリスト
        """
        return [
            name for name, plugin in self._active_plugins.items()
            if plugin.enabled
        ]
    
    def shutdown_all(self):
        """すべてのプラグインを終了"""
        for plugin_name in list(self._active_plugins.keys()):
            self.unload_plugin(plugin_name)
