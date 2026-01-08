"""
メインアプリケーション
"""

from pathlib import Path
from typing import Optional
from .config import ConfigManager
from .events import EventManager
from .theme import ThemeManager
from ..plugins.manager import PluginManager
from ..ui.window import MainWindow
from ..ui.clock import DigitalClock
from ..ui.settings import SettingsWindow
from ..ui.menu import ContextMenu
from ..ui.plugin_manager import PluginManagerWindow
import customtkinter as ctk


class HorloqApp:
    """Horloq メインアプリケーション"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        初期化
        
        Args:
            config_path: 設定ファイルパス（Noneの場合はデフォルト）
        """
        # コアシステムを初期化
        self.config = ConfigManager(config_path)
        self.events = EventManager()
        self.themes = ThemeManager()
        
        # テーマを設定
        theme_name = self.config.get("theme.name", "vscode_dark")
        self.themes.set_theme(theme_name)
        
        # アプリケーションコンテキスト
        self.app_context = {
            "config": self.config,
            "events": self.events,
            "themes": self.themes,
        }
        
        # プラグインマネージャーを初期化
        plugin_dirs = self._get_plugin_dirs()
        self.plugins = PluginManager(self.app_context, plugin_dirs)
        
        # ウィンドウ
        self.window: Optional[MainWindow] = None
        self.clock_widget: Optional[DigitalClock] = None
        self.context_menu: Optional[ContextMenu] = None
        
        # メニューバー要素（テーマ適用用）
        self.menubar: Optional[ctk.CTkFrame] = None
        self.app_label: Optional[ctk.CTkLabel] = None
        self.settings_btn: Optional[ctk.CTkButton] = None
        self.plugin_btn: Optional[ctk.CTkButton] = None
        self.separator: Optional[ctk.CTkFrame] = None
        self.quit_btn: Optional[ctk.CTkButton] = None
        
        # イベントリスナーを登録
        self._setup_event_listeners()
    
    def _get_plugin_dirs(self) -> list[Path]:
        """プラグインディレクトリのリストを取得"""
        # ユーザープラグインディレクトリのみ
        user_plugin_dir = self.config.config_path.parent / "plugins"
        user_plugin_dir.mkdir(parents=True, exist_ok=True)
        return [user_plugin_dir]
    
    def _setup_event_listeners(self):
        """イベントリスナーをセットアップ"""
        self.events.on("app_closing", self._on_app_closing)
        self.events.on("open_settings", self._on_open_settings)
        self.events.on("theme_changed", self._on_theme_changed)
    
    def _on_app_closing(self, event):
        """アプリケーション終了時の処理"""
        # プラグインをシャットダウン
        self.plugins.shutdown_all()
    
    def _on_open_settings(self):
        """設定画面を開く"""
        if self.window:
            SettingsWindow(
                self.window,
                self.config,
                self.themes,
                on_save=self._on_settings_saved,
            )
    
    def _on_settings_saved(self):
        """設定保存時の処理"""
        # テーマを再適用
        theme_name = self.config.get("theme.name", "vscode_dark")
        if self.themes.set_theme(theme_name):
            self.events.emit("theme_changed")
        
        # 時計を更新
        if self.clock_widget:
            self._update_clock_settings()
        
        # ウィンドウ設定を更新
        self.events.emit("config_changed", {"window": True})
    
    def _on_theme_changed(self, event):
        """テーマ変更時の処理"""
        theme = self.themes.current_theme
        
        # 時計ウィジェットにテーマを適用
        if self.clock_widget:
            self.clock_widget.apply_theme(theme)
        
        # メニューバーにテーマを適用
        self._apply_theme_to_menubar()
    
    def _update_clock_settings(self):
        """時計設定を更新"""
        if not self.clock_widget:
            return
        
        # タイムゾーン
        timezone = self.config.get("clock.timezone", "Asia/Tokyo")
        self.clock_widget.set_timezone(timezone)
        
        # フォーマット
        format_24h = self.config.get("clock.format", "24h") == "24h"
        self.clock_widget.set_format(format_24h)
        
        # 秒の表示
        self.clock_widget.show_seconds = self.config.get("clock.show_seconds", True)
        
        # 日付の表示
        show_date = self.config.get("clock.show_date", True)
        self.clock_widget.show_date = show_date
        if show_date and not hasattr(self.clock_widget, 'date_label'):
            # 日付ラベルが存在しない場合は再作成
            self.clock_widget.date_label = ctk.CTkLabel(
                self.clock_widget,
                text="",
                font=("Arial", self.clock_widget.font_size // 3),
            )
            self.clock_widget.date_label.pack()
            self.clock_widget.apply_theme(self.themes.current_theme)
        elif not show_date and hasattr(self.clock_widget, 'date_label'):
            # 日付ラベルを非表示
            self.clock_widget.date_label.pack_forget()
        
        # 日付フォーマット
        self.clock_widget.date_format = self.config.get("clock.date_format", "%Y/%m/%d")
        
        # フォントサイズ
        font_size = self.config.get("clock.font_size", 48)
        self.clock_widget.font_size = font_size
        self.clock_widget.time_label.configure(font=("Arial", font_size, "bold"))
        if hasattr(self.clock_widget, 'date_label'):
            self.clock_widget.date_label.configure(font=("Arial", font_size // 3))
        
        # 即座に表示を更新
        self.clock_widget._update_time()
    
    def _apply_theme_to_menubar(self):
        """メニューバーにテーマを適用"""
        if not self.menubar:
            return
        
        theme = self.themes.current_theme
        
        # メニューバーの背景色
        self.menubar.configure(fg_color=theme.bg_secondary or theme.bg)
        
        # アプリラベルの色
        if self.app_label:
            self.app_label.configure(text_color=theme.accent)
        
        # 設定ボタン
        if self.settings_btn:
            self.settings_btn.configure(
                hover_color=theme.bg,
                text_color=theme.fg,
            )
        
        # プラグインボタン
        if self.plugin_btn:
            self.plugin_btn.configure(
                hover_color=theme.bg,
                text_color=theme.fg,
            )
        
        # セパレータ
        if self.separator:
            self.separator.configure(fg_color=theme.border or "#3e3e42")
    
    def _create_ui(self):
        """UIを作成"""
        # メインウィンドウを作成
        self.window = MainWindow(self.config, self.events, self.themes)
        
        # メニューバー（上部ボタン群）
        theme = self.themes.current_theme
        self.menubar = ctk.CTkFrame(
            self.window, 
            height=45,
            fg_color=theme.bg_secondary or theme.bg,
            corner_radius=8,
        )
        self.menubar.pack(fill="x", padx=8, pady=(8, 5))
        
        # 左側：アプリ名
        self.app_label = ctk.CTkLabel(
            self.menubar,
            text="🕰️ Horloq",
            font=("Arial", 16, "bold"),
            text_color=theme.accent,
        )
        self.app_label.pack(side="left", padx=15, pady=8)
        
        # 右側：ボタン群
        button_frame = ctk.CTkFrame(self.menubar, fg_color="transparent")
        button_frame.pack(side="right", padx=10, pady=6)
        
        # ボタンの共通スタイル
        button_style = {
            "height": 32,
            "corner_radius": 6,
            "font": ("Arial", 12),
            "border_width": 0,
        }
        
        # 設定ボタン
        self.settings_btn = ctk.CTkButton(
            button_frame,
            text="⚙️",
            command=self._on_open_settings,
            width=40,
            fg_color="transparent",
            hover_color=theme.bg,
            text_color=theme.fg,
            **button_style
        )
        self.settings_btn.pack(side="left", padx=3)
        
        # プラグインボタン
        self.plugin_btn = ctk.CTkButton(
            button_frame,
            text="🔌",
            command=self._on_plugin_manager,
            width=40,
            fg_color="transparent",
            hover_color=theme.bg,
            text_color=theme.fg,
            **button_style
        )
        self.plugin_btn.pack(side="left", padx=3)
        
        # セパレータ
        self.separator = ctk.CTkFrame(
            button_frame,
            width=1,
            height=24,
            fg_color=theme.border or "#3e3e42",
        )
        self.separator.pack(side="left", padx=8, pady=4)
        
        # 終了ボタン
        self.quit_btn = ctk.CTkButton(
            button_frame,
            text="✕",
            command=self._on_quit,
            width=40,
            fg_color="#dc3545",
            hover_color="#c82333",
            **button_style
        )
        self.quit_btn.pack(side="left", padx=3)
        
        # コンテナフレーム
        container = ctk.CTkFrame(self.window, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 時計ウィジェット
        self.clock_widget = DigitalClock(
            container,
            timezone=self.config.get("clock.timezone", "Asia/Tokyo"),
            format_24h=self.config.get("clock.format", "24h") == "24h",
            show_seconds=self.config.get("clock.show_seconds", True),
            show_date=self.config.get("clock.show_date", True),
            date_format=self.config.get("clock.date_format", "%Y/%m/%d"),
            font_size=self.config.get("clock.font_size", 48),
            fg_color="transparent",
        )
        self.clock_widget.pack(fill="both", expand=True)
        # 初期テーマを適用
        self.clock_widget.apply_theme(theme)
        
        # プラグインウィジェット用のコンテナ
        self.plugin_container = ctk.CTkFrame(container, fg_color="transparent")
        self.plugin_container.pack(fill="both", expand=False, pady=(10, 0))
    
    def _show_menu_dropdown(self):
        """メニュードロップダウンを表示（将来の拡張用）"""
        # 現在は設定とプラグイン管理が独立したボタンなので、
        # このメニューはその他の機能用に予約
        pass
    
    def _on_plugin_manager(self):
        """プラグイン管理を開く"""
        if self.window:
            PluginManagerWindow(
                self.window,
                self.plugins,
                on_plugin_changed=self._on_plugin_changed,
            )
    
    def _on_plugin_changed(self):
        """プラグイン変更時の処理"""
        # プラグイン設定を保存
        enabled_plugins = self.plugins.list_active_plugins()
        self.config.set("plugins.enabled", enabled_plugins)
        self.config.save()
        
        # プラグインウィジェットを更新
        self._display_plugin_widgets()
        
        # ウィンドウサイズを調整
        self._adjust_window_size()
        
        print(f"有効なプラグイン: {enabled_plugins}")
    
    def _on_quit(self):
        """アプリケーションを終了"""
        if self.window:
            self.window.destroy()
    
    def _load_plugins(self):
        """有効なプラグインを読み込む"""
        enabled_plugins = self.config.get("plugins.enabled", [])
        
        for plugin_name in enabled_plugins:
            if self.plugins.load_plugin(plugin_name):
                print(f"プラグインを読み込みました: {plugin_name}")
            else:
                print(f"プラグインの読み込みに失敗: {plugin_name}")
    
    def _display_plugin_widgets(self):
        """有効なプラグインのウィジェットを表示"""
        if not self.plugin_container:
            return
        
        # 既存のウィジェットをクリア
        for widget in self.plugin_container.winfo_children():
            widget.destroy()
        
        # 有効なプラグインのウィジェットを表示
        active_plugins = self.plugins.list_active_plugins()
        for plugin_name in active_plugins:
            plugin = self.plugins.get_plugin(plugin_name)
            if plugin and plugin.enabled:
                try:
                    widget = plugin.create_widget(self.plugin_container)
                    if widget:
                        widget.pack(fill="both", expand=False, pady=5)
                        print(f"プラグインウィジェットを表示: {plugin_name}")
                except Exception as e:
                    print(f"プラグインウィジェットの表示エラー ({plugin_name}): {e}")
    
    def _adjust_window_size(self):
        """プラグインウィジェットの有無に応じてウィンドウサイズを調整"""
        if not self.window or not self.plugin_container:
            return
        
        # ウィンドウを更新して正確なサイズを取得
        self.window.update_idletasks()
        
        # プラグインウィジェットが存在するか確認
        has_plugin_widgets = len(self.plugin_container.winfo_children()) > 0
        
        # 基本的なウィンドウサイズ（時計のみ）
        base_width = 400
        base_height = 200
        
        if has_plugin_widgets:
            # プラグインウィジェットのサイズを計算
            self.plugin_container.update_idletasks()
            plugin_height = self.plugin_container.winfo_reqheight()
            new_height = base_height + plugin_height + 40  # マージン追加
        else:
            new_height = base_height
        
        # ウィンドウサイズを設定
        self.window.geometry(f"{base_width}x{new_height}")
    
    def run(self):
        """アプリケーションを起動"""
        # プラグインを読み込む
        self._load_plugins()
        
        # UIを作成
        self._create_ui()
        
        # プラグインウィジェットを表示
        self._display_plugin_widgets()
        
        # ウィンドウサイズを調整
        self._adjust_window_size()
        
        # イベントを発行
        self.events.emit("app_started")
        
        # メインループを開始
        if self.window:
            self.window.show()
