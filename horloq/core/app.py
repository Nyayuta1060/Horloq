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
        theme_name = self.config.get("theme.name", "dark")
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
        
        # イベントリスナーを登録
        self._setup_event_listeners()
    
    def _get_plugin_dirs(self) -> list[Path]:
        """プラグインディレクトリのリストを取得"""
        dirs = []
        
        # ビルトインプラグイン
        builtin_dir = Path(__file__).parent / "plugins" / "builtin"
        if builtin_dir.exists():
            dirs.append(builtin_dir)
        
        # ユーザープラグイン
        user_plugin_dir = self.config.config_path.parent / "plugins"
        user_plugin_dir.mkdir(parents=True, exist_ok=True)
        dirs.append(user_plugin_dir)
        
        return dirs
    
    def _setup_event_listeners(self):
        """イベントリスナーをセットアップ"""
        self.events.on("app_closing", self._on_app_closing)
        self.events.on("open_settings", self._on_open_settings)
        self.events.on("theme_changed", self._on_theme_changed)
    
    def _on_app_closing(self, event):
        """アプリケーション終了時の処理"""
        # プラグインをシャットダウン
        self.plugins.shutdown_all()
    
    def _on_open_settings(self, event):
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
        theme_name = self.config.get("theme.name", "dark")
        if self.themes.set_theme(theme_name):
            self.events.emit("theme_changed")
        
        # 時計を更新
        if self.clock_widget:
            self._update_clock_settings()
        
        # ウィンドウ設定を更新
        self.events.emit("config_changed", {"window": True})
    
    def _on_theme_changed(self, event):
        """テーマ変更時の処理"""
        # 時計ウィジェットの再作成が必要な場合
        pass
    
    def _update_clock_settings(self):
        """時計設定を更新"""
        if self.clock_widget:
            # タイムゾーン
            timezone = self.config.get("clock.timezone", "Asia/Tokyo")
            self.clock_widget.set_timezone(timezone)
            
            # フォーマット
            format_24h = self.config.get("clock.format", "24h") == "24h"
            self.clock_widget.set_format(format_24h)
    
    def _create_ui(self):
        """UIを作成"""
        # メインウィンドウを作成
        self.window = MainWindow(self.config, self.events, self.themes)
        
        # コンテナフレーム
        container = ctk.CTkFrame(self.window)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        
        # コンテキストメニューをセットアップ
        self._setup_context_menu()
    
    def _setup_context_menu(self):
        """コンテキストメニューをセットアップ"""
        if not self.window:
            return
        
        self.context_menu = ContextMenu(self.window)
        
        def show_context_menu(event):
            menu_items = [
                ("⚙️ 設定", self._on_open_settings),
                ("---", None),
                ("🔌 プラグイン管理", self._on_plugin_manager),
                ("---", None),
                ("🎨 テーマ", None),  # サブメニューは今後実装
                ("---", None),
                ("❌ 終了", self._on_quit),
            ]
            self.context_menu.show(event, menu_items)
        
        # 右クリックイベントをバインド
        self.window.bind("<Button-3>", show_context_menu)
        if self.clock_widget:
            self.clock_widget.bind("<Button-3>", show_context_menu)
    
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
        enabled_plugins = self.plugins.list_enabled_plugins()
        self.config.set("plugins.enabled", enabled_plugins)
        self.config.save()
        
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
    
    def run(self):
        """アプリケーションを起動"""
        # プラグインを読み込む
        self._load_plugins()
        
        # UIを作成
        self._create_ui()
        
        # イベントを発行
        self.events.emit("app_started")
        
        # メインループを開始
        if self.window:
            self.window.show()
