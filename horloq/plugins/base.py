"""
プラグインベースクラス
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import customtkinter as ctk


class PluginBase(ABC):
    """プラグインの基底クラス"""
    
    # プラグインメタデータ
    name: str = "Unknown Plugin"
    version: str = "0.0.0"
    author: str = "Unknown"
    description: str = ""
    
    def __init__(self, app_context: Dict[str, Any]):
        """
        初期化
        
        Args:
            app_context: アプリケーションコンテキスト
                - config: ConfigManager
                - events: EventManager
                - themes: ThemeManager
        """
        self.app_context = app_context
        self.config = app_context.get("config")
        self.events = app_context.get("events")
        self.themes = app_context.get("themes")
        
        self._widget: Optional[ctk.CTkFrame] = None
        self._enabled = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        プラグインを初期化
        
        Returns:
            初期化成功時True
        """
        pass
    
    @abstractmethod
    def shutdown(self):
        """プラグインを終了"""
        pass
    
    def create_widget(self, parent: ctk.CTkFrame) -> Optional[ctk.CTkFrame]:
        """
        プラグインのウィジェットを作成
        
        Args:
            parent: 親ウィジェット
            
        Returns:
            作成されたウィジェット（ウィジェットがない場合はNone）
        """
        return None
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        プラグイン設定を取得
        
        Args:
            key: 設定キー
            default: デフォルト値
            
        Returns:
            設定値
        """
        plugin_config = self.config.get(f"plugins.configs.{self.name}", {})
        return plugin_config.get(key, default)
    
    def set_config(self, key: str, value: Any):
        """
        プラグイン設定を保存
        
        Args:
            key: 設定キー
            value: 設定値
        """
        plugin_configs = self.config.get("plugins.configs", {})
        if self.name not in plugin_configs:
            plugin_configs[self.name] = {}
        
        plugin_configs[self.name][key] = value
        self.config.set("plugins.configs", plugin_configs)
        self.config.save()
    
    @property
    def enabled(self) -> bool:
        """プラグインが有効かどうか"""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        """プラグインの有効/無効を設定"""
        self._enabled = value
    
    def on_enable(self):
        """プラグインが有効化されたときの処理"""
        pass
    
    def on_disable(self):
        """プラグインが無効化されたときの処理"""
        pass
