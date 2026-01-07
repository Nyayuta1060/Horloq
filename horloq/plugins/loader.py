"""
プラグインローダー
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Type, Optional
from .base import PluginBase


class PluginLoader:
    """プラグインローダー"""
    
    def __init__(self, plugin_dirs: List[Path]):
        """
        初期化
        
        Args:
            plugin_dirs: プラグインディレクトリのリスト
        """
        self.plugin_dirs = plugin_dirs
        self._loaded_plugins: Dict[str, Type[PluginBase]] = {}
    
    def discover_plugins(self) -> List[str]:
        """
        プラグインを検出
        
        Returns:
            検出されたプラグイン名のリスト
        """
        discovered = []
        
        for plugin_dir in self.plugin_dirs:
            if not plugin_dir.exists():
                continue
            
            # ディレクトリ形式のプラグインを検索（__init__.pyを含む）
            for dir_path in plugin_dir.iterdir():
                if not dir_path.is_dir():
                    continue
                if dir_path.name.startswith("_"):
                    continue
                
                # __init__.pyがあればプラグインとして認識
                init_file = dir_path / "__init__.py"
                if init_file.exists():
                    plugin_name = dir_path.name
                    discovered.append(plugin_name)
                    continue
            
            # レガシー形式: 単一Pythonファイル
            for file_path in plugin_dir.glob("*.py"):
                if file_path.name.startswith("_"):
                    continue
                
                plugin_name = file_path.stem
                if plugin_name not in discovered:
                    discovered.append(plugin_name)
        
        return discovered
    
    def load_plugin(self, plugin_name: str) -> Optional[Type[PluginBase]]:
        """
        プラグインを読み込む
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            プラグインクラス（失敗時はNone）
        """
        # すでに読み込まれている場合
        if plugin_name in self._loaded_plugins:
            return self._loaded_plugins[plugin_name]
        
        # プラグインファイルを検索
        plugin_file = self._find_plugin_file(plugin_name)
        if plugin_file is None:
            print(f"プラグインファイルが見つかりません: {plugin_name}")
            return None
        
        try:
            # モジュールを動的に読み込む
            spec = importlib.util.spec_from_file_location(
                f"horloq_plugin_{plugin_name}",
                plugin_file
            )
            if spec is None or spec.loader is None:
                print(f"プラグインの読み込みに失敗: {plugin_name}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            
            # プラグインクラスを検索
            plugin_class = self._find_plugin_class(module)
            if plugin_class is None:
                print(f"プラグインクラスが見つかりません: {plugin_name}")
                return None
            
            self._loaded_plugins[plugin_name] = plugin_class
            return plugin_class
            
        except Exception as e:
            print(f"プラグインの読み込みエラー ({plugin_name}): {e}")
            return None
    
    def unload_plugin(self, plugin_name: str):
        """
        プラグインをアンロード
        
        Args:
            plugin_name: プラグイン名
        """
        if plugin_name in self._loaded_plugins:
            del self._loaded_plugins[plugin_name]
        
        # sys.modulesからも削除
        module_name = f"horloq_plugin_{plugin_name}"
        if module_name in sys.modules:
            del sys.modules[module_name]
    
    def _find_plugin_file(self, plugin_name: str) -> Optional[Path]:
        """
        プラグインファイルを検索
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            プラグインファイルのパス（見つからない場合はNone）
        """
        for plugin_dir in self.plugin_dirs:
            # ディレクトリ形式（優先）
            plugin_package = plugin_dir / plugin_name
            if plugin_package.is_dir():
                init_file = plugin_package / "__init__.py"
                if init_file.exists():
                    return init_file
            
            # 単一ファイル形式（レガシー）
            plugin_file = plugin_dir / f"{plugin_name}.py"
            if plugin_file.exists():
                return plugin_file
        
        return None
    
    def _find_plugin_class(self, module) -> Optional[Type[PluginBase]]:
        """
        モジュールからプラグインクラスを検索
        
        Args:
            module: Pythonモジュール
            
        Returns:
            プラグインクラス（見つからない場合はNone）
        """
        # まず、'Plugin'という名前のエクスポートを確認（推奨）
        if hasattr(module, 'Plugin'):
            plugin_class = getattr(module, 'Plugin')
            if (isinstance(plugin_class, type) and 
                issubclass(plugin_class, PluginBase) and 
                plugin_class is not PluginBase):
                return plugin_class
        
        # 次に、PluginBaseのサブクラスを検索
        for name in dir(module):
            obj = getattr(module, name)
            
            # クラスであり、PluginBaseのサブクラスである
            if (isinstance(obj, type) and 
                issubclass(obj, PluginBase) and 
                obj is not PluginBase):
                return obj
        
        return None
    
    @property
    def loaded_plugins(self) -> Dict[str, Type[PluginBase]]:
        """読み込まれたプラグインのリスト"""
        return self._loaded_plugins
