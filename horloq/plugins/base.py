"""
プラグインベースクラス
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path
import customtkinter as ctk
import yaml


class PluginBase(ABC):
    """プラグインの基底クラス"""
    
    def __init__(
        self, 
        app_context: Dict[str, Any],
        name: str = "Unknown Plugin",
        version: str = "0.0.0",
        author: str = "Unknown",
        description: str = "",
    ):
        """
        初期化
        
        Args:
            app_context: アプリケーションコンテキスト
                - config: ConfigManager
                - events: EventManager
                - themes: ThemeManager
            name: プラグイン名（省略可：plugin.yamlから自動読み込み）
            version: バージョン（省略可：plugin.yamlから自動読み込み）
            author: 作者（省略可：plugin.yamlから自動読み込み）
            description: 説明（省略可：plugin.yamlから自動読み込み）
        """
        # plugin.yamlからメタデータを読み込む（ハードコーディングよりも優先）
        metadata = self._load_plugin_metadata()
        
        self.name = metadata.get('name', name)
        self.version = metadata.get('version', version)
        self.author = metadata.get('author', author)
        self.description = metadata.get('description', description)
        
        self.app_context = app_context
        self.config = app_context.get("config")
        self.events = app_context.get("events")
        self.themes = app_context.get("themes")
        
        self._widget: Optional[ctk.CTkFrame] = None
        self._enabled = False
    
    def _load_plugin_metadata(self) -> Dict[str, Any]:
        """
        plugin.yamlからメタデータを読み込む
        
        Returns:
            メタデータの辞書
        """
        try:
            # プラグインクラスのファイルパスから plugin.yaml を探す
            import inspect
            class_file = Path(inspect.getfile(self.__class__))
            plugin_dir = class_file.parent
            plugin_yaml = plugin_dir / "plugin.yaml"
            
            if plugin_yaml.exists():
                with open(plugin_yaml, 'r', encoding='utf-8') as f:
                    metadata = yaml.safe_load(f)
                    if metadata:
                        return metadata
        except Exception as e:
            # エラーが発生してもフォールバック
            pass
        
        return {}
    
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
