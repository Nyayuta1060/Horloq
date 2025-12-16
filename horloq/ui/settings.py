"""
設定画面UI
"""

import customtkinter as ctk
from typing import Callable, Optional
from ..core.config import ConfigManager
from ..core.theme import ThemeManager


class SettingsWindow(ctk.CTkToplevel):
    """設定ウィンドウ"""
    
    def __init__(
        self,
        master,
        config_manager: ConfigManager,
        theme_manager: ThemeManager,
        on_save: Optional[Callable] = None,
    ):
        """
        初期化
        
        Args:
            master: 親ウィンドウ
            config_manager: 設定マネージャー
            theme_manager: テーママネージャー
            on_save: 保存時のコールバック
        """
        super().__init__(master)
        
        self.config = config_manager
        self.themes = theme_manager
        self.on_save = on_save
        
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self):
        """ウィンドウをセットアップ"""
        self.title("設定")
        self.geometry("600x500")
        
        # モーダルウィンドウとして表示
        self.transient(self.master)
        self.grab_set()
    
    def _create_widgets(self):
        """ウィジェットを作成"""
        # タブビュー
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 各タブを追加
        self.tabview.add("一般")
        self.tabview.add("時計")
        self.tabview.add("テーマ")
        self.tabview.add("ウィンドウ")
        
        # 各タブの内容を作成
        self._create_general_tab()
        self._create_clock_tab()
        self._create_theme_tab()
        self._create_window_tab()
        
        # ボタンフレーム
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # 保存ボタン
        save_btn = ctk.CTkButton(
            button_frame,
            text="保存",
            command=self._save_settings,
        )
        save_btn.pack(side="right", padx=5)
        
        # キャンセルボタン
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="キャンセル",
            command=self.destroy,
        )
        cancel_btn.pack(side="right", padx=5)
    
    def _create_general_tab(self):
        """一般タブを作成"""
        tab = self.tabview.tab("一般")
        
        # 自動起動
        self.auto_start_var = ctk.BooleanVar(
            value=self.config.get("general.auto_start", False)
        )
        auto_start_check = ctk.CTkCheckBox(
            tab,
            text="起動時に自動実行",
            variable=self.auto_start_var,
        )
        auto_start_check.pack(anchor="w", padx=20, pady=10)
        
        # 更新チェック
        self.check_updates_var = ctk.BooleanVar(
            value=self.config.get("general.check_updates", True)
        )
        check_updates_check = ctk.CTkCheckBox(
            tab,
            text="起動時に更新を確認",
            variable=self.check_updates_var,
        )
        check_updates_check.pack(anchor="w", padx=20, pady=10)
    
    def _create_clock_tab(self):
        """時計タブを作成"""
        tab = self.tabview.tab("時計")
        
        # 24時間形式
        self.format_24h_var = ctk.BooleanVar(
            value=self.config.get("clock.format") == "24h"
        )
        format_check = ctk.CTkCheckBox(
            tab,
            text="24時間形式",
            variable=self.format_24h_var,
        )
        format_check.pack(anchor="w", padx=20, pady=10)
        
        # 秒を表示
        self.show_seconds_var = ctk.BooleanVar(
            value=self.config.get("clock.show_seconds", True)
        )
        seconds_check = ctk.CTkCheckBox(
            tab,
            text="秒を表示",
            variable=self.show_seconds_var,
        )
        seconds_check.pack(anchor="w", padx=20, pady=10)
        
        # 日付を表示
        self.show_date_var = ctk.BooleanVar(
            value=self.config.get("clock.show_date", True)
        )
        date_check = ctk.CTkCheckBox(
            tab,
            text="日付を表示",
            variable=self.show_date_var,
        )
        date_check.pack(anchor="w", padx=20, pady=10)
        
        # フォントサイズ
        font_frame = ctk.CTkFrame(tab)
        font_frame.pack(fill="x", padx=20, pady=10)
        
        font_label = ctk.CTkLabel(font_frame, text="フォントサイズ:")
        font_label.pack(side="left", padx=5)
        
        self.font_size_var = ctk.IntVar(
            value=self.config.get("clock.font_size", 48)
        )
        font_slider = ctk.CTkSlider(
            font_frame,
            from_=24,
            to=96,
            variable=self.font_size_var,
        )
        font_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        font_value_label = ctk.CTkLabel(
            font_frame,
            textvariable=self.font_size_var,
            width=40,
        )
        font_value_label.pack(side="left", padx=5)
    
    def _create_theme_tab(self):
        """テーマタブを作成"""
        tab = self.tabview.tab("テーマ")
        
        # テーマ選択
        theme_label = ctk.CTkLabel(tab, text="テーマ:")
        theme_label.pack(anchor="w", padx=20, pady=10)
        
        current_theme = self.config.get("theme.name", "dark")
        themes = self.themes.list_themes()
        
        self.theme_var = ctk.StringVar(value=current_theme)
        theme_menu = ctk.CTkOptionMenu(
            tab,
            values=themes,
            variable=self.theme_var,
        )
        theme_menu.pack(fill="x", padx=20, pady=5)
    
    def _create_window_tab(self):
        """ウィンドウタブを作成"""
        tab = self.tabview.tab("ウィンドウ")
        
        # 常に最前面
        self.always_on_top_var = ctk.BooleanVar(
            value=self.config.get("window.always_on_top", True)
        )
        topmost_check = ctk.CTkCheckBox(
            tab,
            text="常に最前面に表示",
            variable=self.always_on_top_var,
        )
        topmost_check.pack(anchor="w", padx=20, pady=10)
        
        # 不透明度
        opacity_frame = ctk.CTkFrame(tab)
        opacity_frame.pack(fill="x", padx=20, pady=10)
        
        opacity_label = ctk.CTkLabel(opacity_frame, text="不透明度:")
        opacity_label.pack(side="left", padx=5)
        
        self.opacity_var = ctk.DoubleVar(
            value=self.config.get("window.opacity", 1.0)
        )
        opacity_slider = ctk.CTkSlider(
            opacity_frame,
            from_=0.3,
            to=1.0,
            variable=self.opacity_var,
        )
        opacity_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        opacity_value_label = ctk.CTkLabel(
            opacity_frame,
            textvariable=self.opacity_var,
            width=40,
        )
        opacity_value_label.pack(side="left", padx=5)
    
    def _save_settings(self):
        """設定を保存"""
        # 一般設定
        self.config.set("general.auto_start", self.auto_start_var.get())
        self.config.set("general.check_updates", self.check_updates_var.get())
        
        # 時計設定
        self.config.set("clock.format", "24h" if self.format_24h_var.get() else "12h")
        self.config.set("clock.show_seconds", self.show_seconds_var.get())
        self.config.set("clock.show_date", self.show_date_var.get())
        self.config.set("clock.font_size", self.font_size_var.get())
        
        # テーマ設定
        self.config.set("theme.name", self.theme_var.get())
        
        # ウィンドウ設定
        self.config.set("window.always_on_top", self.always_on_top_var.get())
        self.config.set("window.opacity", self.opacity_var.get())
        
        # 設定を保存
        self.config.save()
        
        # コールバックを呼び出す
        if self.on_save:
            self.on_save()
        
        # ウィンドウを閉じる
        self.destroy()
