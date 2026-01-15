"""
設定管理システム
"""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from copy import deepcopy


class ConfigManager:
    """アプリケーション設定管理"""
    
    DEFAULT_CONFIG = {
        "window": {
            "width": 400,
            "height": 200,
            "x": None,
            "y": None,
            "always_on_top": True,
            "transparent": False,
            "opacity": 1.0,
        },
        "clock": {
            "format": "24h",  # "12h" or "24h"
            "show_seconds": True,
            "show_milliseconds": False,
            "show_date": True,
            "show_weekday": True,
            "date_format": "%Y/%m/%d",
            "timezone": "Asia/Tokyo",
            "font_size": 48,
            "font_family": "Arial",
        },
        "theme": {
            "name": "vscode_dark",
            "custom_colors": {
                "bg": "#1e1e1e",
                "fg": "#d4d4d4",
                "accent": "#007acc",
            },
        },
        "plugins": {
            "enabled": [],
            "configs": {},
        },
        "general": {
            "language": "ja",
            "auto_start": False,
            "check_updates": True,
        },
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        初期化
        
        Args:
            config_path: 設定ファイルのパス（Noneの場合はデフォルトパスを使用）
        """
        if config_path is None:
            config_path = self._get_default_config_path()
        
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load()
    
    @staticmethod
    def _get_default_config_path() -> Path:
        """デフォルト設定ファイルパスを取得"""
        import platform
        
        system = platform.system()
        home = Path.home()
        
        if system == "Windows":
            config_dir = home / "AppData" / "Local" / "Horloq"
        elif system == "Darwin":  # macOS
            config_dir = home / "Library" / "Application Support" / "Horloq"
        else:  # Linux
            config_dir = home / ".config" / "horloq"
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.yaml"
    
    def load(self):
        """設定ファイルを読み込む"""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded_config = yaml.safe_load(f) or {}
                # デフォルト設定にマージ
                self.config = self._merge_config(self.DEFAULT_CONFIG, loaded_config)
            except Exception as e:
                print(f"設定ファイルの読み込みに失敗しました: {e}")
                self.config = deepcopy(self.DEFAULT_CONFIG)
        else:
            self.config = deepcopy(self.DEFAULT_CONFIG)
            self.save()
    
    def save(self):
        """設定ファイルに保存"""
        try:
            # ディレクトリが存在しない場合は作成
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            print(f"設定ファイルの保存に失敗しました: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        設定値を取得（ドット記法対応）
        
        Args:
            key: 設定キー（例: "window.width"）
            default: デフォルト値
            
        Returns:
            設定値
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        設定値を設定（ドット記法対応）
        
        Args:
            key: 設定キー（例: "window.width"）
            value: 設定値
        """
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def reset(self):
        """設定をデフォルトにリセット"""
        self.config = deepcopy(self.DEFAULT_CONFIG)
        self.save()
    
    def _merge_config(self, default: Dict, loaded: Dict) -> Dict:
        """
        デフォルト設定と読み込んだ設定をマージ
        
        Args:
            default: デフォルト設定
            loaded: 読み込んだ設定
            
        Returns:
            マージされた設定
        """
        result = deepcopy(default)
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def export_config(self, export_path: Path):
        """
        設定をファイルにエクスポート
        
        Args:
            export_path: エクスポート先のパス
        
        Raises:
            Exception: エクスポートに失敗した場合
        """
        try:
            # ディレクトリが存在しない場合は作成
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_path, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            raise Exception(f"設定のエクスポートに失敗しました: {e}")
    
    def import_config(self, import_path: Path):
        """
        設定をファイルからインポート
        
        Args:
            import_path: インポート元のパス
        
        Raises:
            Exception: インポートに失敗した場合
        """
        try:
            if not import_path.exists():
                raise FileNotFoundError(f"ファイルが見つかりません: {import_path}")
            
            with open(import_path, "r", encoding="utf-8") as f:
                loaded_config = yaml.safe_load(f) or {}
            
            # デフォルト設定にマージ
            self.config = self._merge_config(self.DEFAULT_CONFIG, loaded_config)
            
            # 現在の設定ファイルに保存
            self.save()
        except Exception as e:
            raise Exception(f"設定のインポートに失敗しました: {e}")
