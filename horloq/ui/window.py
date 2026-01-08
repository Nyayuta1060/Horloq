"""
メインウィンドウ管理
"""

import customtkinter as ctk
from typing import Optional
from ..core.config import ConfigManager
from ..core.events import EventManager
from ..core.theme import ThemeManager


class MainWindow(ctk.CTk):
    """メインウィンドウ"""
    
    def __init__(
        self,
        config_manager: ConfigManager,
        event_manager: EventManager,
        theme_manager: ThemeManager,
    ):
        """
        初期化
        
        Args:
            config_manager: 設定マネージャー
            event_manager: イベントマネージャー
            theme_manager: テーママネージャー
        """
        super().__init__()
        
        self.config = config_manager
        self.events = event_manager
        self.themes = theme_manager
        
        self._setup_window()
        self._apply_theme()
        
        # イベントリスナーを登録
        self.events.on("theme_changed", self._on_theme_changed)
        self.events.on("config_changed", self._on_config_changed)
    
    def _setup_window(self):
        """ウィンドウをセットアップ"""
        # ウィンドウタイトル
        self.title("Horloq")
        
        # ウィンドウサイズと位置
        width = self.config.get("window.width", 400)
        height = self.config.get("window.height", 250)
        x = self.config.get("window.x")
        y = self.config.get("window.y")
        
        if x is not None and y is not None:
            self.geometry(f"{width}x{height}+{x}+{y}")
        else:
            self.geometry(f"{width}x{height}")
            # 画面中央に配置
            self._center_window()
        
        # 常に最前面
        if self.config.get("window.always_on_top", True):
            self.attributes("-topmost", True)
        
        # 透明度
        opacity = self.config.get("window.opacity", 1.0)
        self.attributes("-alpha", opacity)
        
        # ウィンドウを閉じるときのイベント
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _center_window(self):
        """ウィンドウを画面中央に配置"""
        self.update_idletasks()
        
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f"+{x}+{y}")
    
    def _apply_theme(self):
        """テーマを適用"""
        theme = self.themes.current_theme
        
        # CustomTkinterのテーマモード設定（light/darkの判定を改善）
        is_dark = theme.name.lower() != "light"
        ctk.set_appearance_mode("dark" if is_dark else "light")
        
        # 背景色とテキスト色を設定
        self.configure(fg_color=theme.bg)
        
        # デフォルトカラーをオーバーライド
        ctk.ThemeManager.theme["CTk"]["fg_color"] = [theme.bg, theme.bg]
        ctk.ThemeManager.theme["CTkFrame"]["fg_color"] = [theme.bg_secondary or theme.bg, theme.bg_secondary or theme.bg]
        ctk.ThemeManager.theme["CTkLabel"]["text_color"] = [theme.fg, theme.fg]
        ctk.ThemeManager.theme["CTkButton"]["fg_color"] = [theme.accent, theme.accent]
        ctk.ThemeManager.theme["CTkButton"]["hover_color"] = [theme.hover or theme.accent, theme.hover or theme.accent]
        ctk.ThemeManager.theme["CTkButton"]["text_color"] = [theme.fg, theme.fg]
    
    def _on_theme_changed(self, event):
        """テーマ変更イベント処理"""
        self._apply_theme()
    
    def _on_config_changed(self, event):
        """設定変更イベント処理"""
        # ウィンドウ設定の更新
        if event.data and "window" in event.data:
            self._setup_window()
    
    def _on_close(self):
        """ウィンドウを閉じる処理"""
        # 現在の位置を保存
        self.config.set("window.x", self.winfo_x())
        self.config.set("window.y", self.winfo_y())
        self.config.save()
        
        # イベントを発行
        self.events.emit("app_closing")
        
        # ウィンドウを破棄
        self.destroy()
    
    def show(self):
        """ウィンドウを表示"""
        self.mainloop()
