"""
テーマ管理システム
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class Theme:
    """テーマデータ"""
    name: str
    bg: str
    fg: str
    accent: str
    bg_secondary: Optional[str] = None
    fg_secondary: Optional[str] = None
    border: Optional[str] = None
    hover: Optional[str] = None


class ThemeManager:
    """テーマ管理"""
    
    BUILTIN_THEMES = {
        "dark": Theme(
            name="Dark",
            bg="#1a1a1a",
            fg="#ffffff",
            accent="#00a8ff",
            bg_secondary="#2a2a2a",
            fg_secondary="#cccccc",
            border="#3a3a3a",
            hover="#00d4ff",
        ),
        "light": Theme(
            name="Light",
            bg="#ffffff",
            fg="#1a1a1a",
            accent="#0078d4",
            bg_secondary="#f5f5f5",
            fg_secondary="#333333",
            border="#e0e0e0",
            hover="#0086f0",
        ),
        "nord": Theme(
            name="Nord",
            bg="#2e3440",
            fg="#eceff4",
            accent="#88c0d0",
            bg_secondary="#3b4252",
            fg_secondary="#d8dee9",
            border="#4c566a",
            hover="#8fbcbb",
        ),
        "dracula": Theme(
            name="Dracula",
            bg="#282a36",
            fg="#f8f8f2",
            accent="#bd93f9",
            bg_secondary="#44475a",
            fg_secondary="#f8f8f2",
            border="#6272a4",
            hover="#ff79c6",
        ),
    }
    
    def __init__(self):
        """初期化"""
        self._current_theme: Theme = self.BUILTIN_THEMES["dark"]
        self._custom_themes: Dict[str, Theme] = {}
    
    def get_theme(self, theme_name: str) -> Optional[Theme]:
        """
        テーマを取得
        
        Args:
            theme_name: テーマ名
            
        Returns:
            テーマ（存在しない場合はNone）
        """
        if theme_name in self.BUILTIN_THEMES:
            return self.BUILTIN_THEMES[theme_name]
        
        return self._custom_themes.get(theme_name)
    
    def set_theme(self, theme_name: str) -> bool:
        """
        現在のテーマを設定
        
        Args:
            theme_name: テーマ名
            
        Returns:
            成功した場合True
        """
        theme = self.get_theme(theme_name)
        if theme is None:
            return False
        
        self._current_theme = theme
        return True
    
    @property
    def current_theme(self) -> Theme:
        """現在のテーマを取得"""
        return self._current_theme
    
    def add_custom_theme(self, theme_name: str, theme: Theme):
        """
        カスタムテーマを追加
        
        Args:
            theme_name: テーマ名
            theme: テーマデータ
        """
        self._custom_themes[theme_name] = theme
    
    def remove_custom_theme(self, theme_name: str):
        """
        カスタムテーマを削除
        
        Args:
            theme_name: テーマ名
        """
        if theme_name in self._custom_themes:
            del self._custom_themes[theme_name]
    
    def list_themes(self) -> list[str]:
        """
        利用可能なテーマ名のリストを取得
        
        Returns:
            テーマ名のリスト
        """
        builtin = list(self.BUILTIN_THEMES.keys())
        custom = list(self._custom_themes.keys())
        return builtin + custom
    
    def create_theme_from_colors(
        self,
        name: str,
        bg: str,
        fg: str,
        accent: str,
        **kwargs
    ) -> Theme:
        """
        色指定からテーマを作成
        
        Args:
            name: テーマ名
            bg: 背景色
            fg: 前景色
            accent: アクセント色
            **kwargs: その他のオプション
            
        Returns:
            作成されたテーマ
        """
        return Theme(
            name=name,
            bg=bg,
            fg=fg,
            accent=accent,
            bg_secondary=kwargs.get("bg_secondary"),
            fg_secondary=kwargs.get("fg_secondary"),
            border=kwargs.get("border"),
            hover=kwargs.get("hover"),
        )
