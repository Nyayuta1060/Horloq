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
        self.geometry("650x600")
        
        # モーダルウィンドウとして表示
        self.transient(self.master)
        
        # ウィンドウを表示してからgrab_setを呼ぶ
        self.update_idletasks()
        self.after(10, self.grab_set)
    
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
        
        # 設定のエクスポート/インポート
        import_export_label = ctk.CTkLabel(tab, text="設定のバックアップ:", font=("Arial", 14, "bold"))
        import_export_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        export_btn = ctk.CTkButton(
            button_frame,
            text="設定をエクスポート",
            command=self._export_config,
        )
        export_btn.pack(side="left", padx=5)
        
        import_btn = ctk.CTkButton(
            button_frame,
            text="設定をインポート",
            command=self._import_config,
        )
        import_btn.pack(side="left", padx=5)
    
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
        
        # ミリ秒を表示
        self.show_milliseconds_var = ctk.BooleanVar(
            value=self.config.get("clock.show_milliseconds", False)
        )
        milliseconds_check = ctk.CTkCheckBox(
            tab,
            text="ミリ秒を表示",
            variable=self.show_milliseconds_var,
        )
        milliseconds_check.pack(anchor="w", padx=20, pady=10)
        
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
        
        # 曜日を表示
        self.show_weekday_var = ctk.BooleanVar(
            value=self.config.get("clock.show_weekday", True)
        )
        weekday_check = ctk.CTkCheckBox(
            tab,
            text="曜日を表示",
            variable=self.show_weekday_var,
        )
        weekday_check.pack(anchor="w", padx=20, pady=10)
        
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
        
        # フォントファミリー
        font_family_frame = ctk.CTkFrame(tab)
        font_family_frame.pack(fill="x", padx=20, pady=10)
        
        font_family_label = ctk.CTkLabel(font_family_frame, text="フォント:")
        font_family_label.pack(side="left", padx=5)
        
        available_fonts = ["Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana", "Georgia", "Comic Sans MS", "Trebuchet MS", "Impact"]
        self.font_family_var = ctk.StringVar(
            value=self.config.get("clock.font_family", "Arial")
        )
        font_family_menu = ctk.CTkOptionMenu(
            font_family_frame,
            values=available_fonts,
            variable=self.font_family_var,
        )
        font_family_menu.pack(side="left", fill="x", expand=True, padx=5)
    
    def _create_theme_tab(self):
        """テーマタブを作成"""
        tab = self.tabview.tab("テーマ")
        
        # テーマ選択
        theme_label = ctk.CTkLabel(tab, text="テーマ:", font=("Arial", 14, "bold"))
        theme_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        current_theme = self.config.get("theme.name", "vscode_dark")
        themes = self.themes.list_themes()
        
        self.theme_var = ctk.StringVar(value=current_theme)
        theme_menu = ctk.CTkOptionMenu(
            tab,
            values=themes,
            variable=self.theme_var,
            command=self._on_theme_change,
        )
        theme_menu.pack(fill="x", padx=20, pady=5)
        
        # プレビューフレーム
        preview_label = ctk.CTkLabel(tab, text="プレビュー:", font=("Arial", 14, "bold"))
        preview_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.preview_frame = ctk.CTkFrame(tab, height=200)
        self.preview_frame.pack(fill="x", padx=20, pady=5)
        self.preview_frame.pack_propagate(False)
        
        # プレビューを更新
        self._update_theme_preview()
    
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
        
        # 0-100%の整数値で管理
        current_opacity = self.config.get("window.opacity", 1.0)
        self.opacity_var = ctk.IntVar(
            value=int(current_opacity * 100)
        )
        opacity_slider = ctk.CTkSlider(
            opacity_frame,
            from_=30,
            to=100,
            variable=self.opacity_var,
            number_of_steps=70,
        )
        opacity_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        # パーセント表示用のラベル
        self.opacity_display_var = ctk.StringVar(value=f"{self.opacity_var.get()}%")
        opacity_value_label = ctk.CTkLabel(
            opacity_frame,
            textvariable=self.opacity_display_var,
            width=50,
        )
        opacity_value_label.pack(side="left", padx=5)
        
        # スライダー変更時に表示を更新
        def update_opacity_display(*args):
            self.opacity_display_var.set(f"{self.opacity_var.get()}%")
        self.opacity_var.trace_add("write", update_opacity_display)
    
    def _on_theme_change(self, theme_name: str):
        """テーマ変更イベント処理"""
        self._update_theme_preview()
    
    def _update_theme_preview(self):
        """テーマプレビューを更新"""
        # 既存のウィジェットをクリア
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        # 選択されたテーマを取得
        theme_name = self.theme_var.get()
        theme = self.themes.get_theme(theme_name)
        
        if not theme:
            return
        
        # プレビューフレームの背景色を設定
        self.preview_frame.configure(fg_color=theme.bg)
        
        # サンプルテキスト
        sample_frame = ctk.CTkFrame(
            self.preview_frame,
            fg_color=theme.bg_secondary,
            border_color=theme.border,
            border_width=2,
        )
        sample_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # タイトル
        title = ctk.CTkLabel(
            sample_frame,
            text="23:45:30",
            font=("Arial", 36, "bold"),
            text_color=theme.fg,
        )
        title.pack(pady=(20, 5))
        
        # サブタイトル
        subtitle = ctk.CTkLabel(
            sample_frame,
            text="2026年1月6日",
            font=("Arial", 14),
            text_color=theme.fg_secondary,
        )
        subtitle.pack(pady=(0, 10))
        
        # アクセントボタン
        button = ctk.CTkButton(
            sample_frame,
            text="アクセントカラー",
            fg_color=theme.accent,
            hover_color=theme.hover,
            text_color=theme.bg,
        )
        button.pack(pady=(5, 20))
    
    def _save_settings(self):
        """設定を保存"""
        # 一般設定
        self.config.set("general.auto_start", self.auto_start_var.get())
        self.config.set("general.check_updates", self.check_updates_var.get())
        
        # 時計設定
        self.config.set("clock.format", "24h" if self.format_24h_var.get() else "12h")
        self.config.set("clock.show_seconds", self.show_seconds_var.get())
        self.config.set("clock.show_milliseconds", self.show_milliseconds_var.get())
        self.config.set("clock.show_date", self.show_date_var.get())
        self.config.set("clock.show_weekday", self.show_weekday_var.get())
        self.config.set("clock.font_size", self.font_size_var.get())
        self.config.set("clock.font_family", self.font_family_var.get())
        
        # テーマ設定
        self.config.set("theme.name", self.theme_var.get())
        
        # ウィンドウ設定
        self.config.set("window.always_on_top", self.always_on_top_var.get())
        # 不透明度を0-1の範囲に変換（整数パーセント → 小数点）
        self.config.set("window.opacity", self.opacity_var.get() / 100.0)
        
        # 設定を保存
        self.config.save()
        
        # コールバックを呼び出す
        if self.on_save:
            self.on_save()
        
        # ウィンドウを閉じる
        self.destroy()
    
    def _export_config(self):
        """設定をエクスポート"""
        from tkinter import filedialog
        from pathlib import Path
        
        # ファイル保存ダイアログを表示
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="設定をエクスポート",
            defaultextension=".yaml",
            filetypes=[("YAMLファイル", "*.yaml *.yml"), ("すべてのファイル", "*.*")],
        )
        
        if file_path:
            try:
                self.config.export_config(Path(file_path))
                # 成功メッセージを表示
                self._show_message("成功", "設定をエクスポートしました")
            except Exception as e:
                self._show_message("エラー", f"エクスポートに失敗しました: {e}")
    
    def _import_config(self):
        """設定をインポート"""
        from tkinter import filedialog
        from pathlib import Path
        
        # ファイル選択ダイアログを表示
        file_path = filedialog.askopenfilename(
            parent=self,
            title="設定をインポート",
            filetypes=[("YAMLファイル", "*.yaml *.yml"), ("すべてのファイル", "*.*")],
        )
        
        if file_path:
            try:
                self.config.import_config(Path(file_path))
                # 成功メッセージを表示
                self._show_message("成功", "設定をインポートしました\nアプリを再起動してください")
            except Exception as e:
                self._show_message("エラー", f"インポートに失敗しました: {e}")
    
    def _show_message(self, title: str, message: str):
        """メッセージダイアログを表示"""
        from tkinter import messagebox
        messagebox.showinfo(title, message, parent=self)
