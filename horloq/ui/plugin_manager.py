"""
プラグイン管理UI
"""

import customtkinter as ctk
from typing import Callable, Optional
from ..plugins.manager import PluginManager


class PluginManagerWindow(ctk.CTkToplevel):
    """プラグイン管理ウィンドウ"""
    
    def __init__(
        self,
        master,
        plugin_manager: PluginManager,
        on_plugin_changed: Optional[Callable] = None,
    ):
        """
        初期化
        
        Args:
            master: 親ウィンドウ
            plugin_manager: プラグインマネージャー
            on_plugin_changed: プラグイン変更時のコールバック
        """
        super().__init__(master)
        
        self.plugin_manager = plugin_manager
        self.on_plugin_changed = on_plugin_changed
        
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self):
        """ウィンドウをセットアップ"""
        self.title("プラグイン管理")
        self.geometry("600x500")
        
        # モーダルウィンドウとして表示
        self.transient(self.master)
        self.grab_set()
    
    def _create_widgets(self):
        """ウィジェットを作成"""
        # タイトル
        title_label = ctk.CTkLabel(
            self,
            text="🔌 プラグイン管理",
            font=("Arial", 20, "bold"),
        )
        title_label.pack(pady=20)
        
        # 説明
        desc_label = ctk.CTkLabel(
            self,
            text="利用可能なプラグインの一覧です。チェックボックスで有効/無効を切り替えできます。",
            font=("Arial", 12),
        )
        desc_label.pack(pady=(0, 20))
        
        # プラグインリスト
        list_frame = ctk.CTkScrollableFrame(self, height=300)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # 利用可能なプラグインを取得
        available_plugins = self.plugin_manager.discover_plugins()
        active_plugins = self.plugin_manager.list_active_plugins()
        enabled_plugins = self.plugin_manager.list_enabled_plugins()
        
        if not available_plugins:
            no_plugin_label = ctk.CTkLabel(
                list_frame,
                text="プラグインが見つかりませんでした",
                font=("Arial", 14),
            )
            no_plugin_label.pack(pady=20)
        else:
            for plugin_name in available_plugins:
                self._create_plugin_item(
                    list_frame,
                    plugin_name,
                    plugin_name in enabled_plugins,
                )
        
        # ボタンフレーム
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # 閉じるボタン
        close_btn = ctk.CTkButton(
            button_frame,
            text="閉じる",
            command=self.destroy,
        )
        close_btn.pack(side="right", padx=5)
        
        # 再読み込みボタン
        reload_btn = ctk.CTkButton(
            button_frame,
            text="🔄 再読み込み",
            command=self._reload_plugins,
            fg_color="gray",
            hover_color="darkgray",
        )
        reload_btn.pack(side="right", padx=5)
    
    def _create_plugin_item(self, parent, plugin_name: str, is_enabled: bool):
        """プラグインアイテムを作成"""
        item_frame = ctk.CTkFrame(parent)
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # チェックボックス
        var = ctk.BooleanVar(value=is_enabled)
        checkbox = ctk.CTkCheckBox(
            item_frame,
            text="",
            variable=var,
            command=lambda: self._toggle_plugin(plugin_name, var.get()),
        )
        checkbox.pack(side="left", padx=10, pady=10)
        
        # プラグイン情報
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        # プラグイン名
        name_label = ctk.CTkLabel(
            info_frame,
            text=plugin_name,
            font=("Arial", 14, "bold"),
            anchor="w",
        )
        name_label.pack(anchor="w")
        
        # プラグインの詳細情報を取得
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if plugin:
            desc_text = f"{plugin.description} (v{plugin.version} by {plugin.author})"
        else:
            desc_text = "プラグインの説明がありません"
        
        desc_label = ctk.CTkLabel(
            info_frame,
            text=desc_text,
            font=("Arial", 11),
            text_color="gray70",
            anchor="w",
        )
        desc_label.pack(anchor="w")
    
    def _toggle_plugin(self, plugin_name: str, enable: bool):
        """プラグインの有効/無効を切り替え"""
        try:
            if enable:
                success = self.plugin_manager.enable_plugin(plugin_name)
                if success:
                    print(f"プラグイン '{plugin_name}' を有効化しました")
                else:
                    print(f"プラグイン '{plugin_name}' の有効化に失敗しました")
            else:
                success = self.plugin_manager.disable_plugin(plugin_name)
                if success:
                    print(f"プラグイン '{plugin_name}' を無効化しました")
                else:
                    print(f"プラグイン '{plugin_name}' の無効化に失敗しました")
            
            # コールバックを呼び出す
            if self.on_plugin_changed:
                self.on_plugin_changed()
                
        except Exception as e:
            print(f"プラグイン操作エラー: {e}")
    
    def _reload_plugins(self):
        """プラグインリストを再読み込み"""
        # ウィンドウを閉じて再度開く
        self.destroy()
        PluginManagerWindow(
            self.master,
            self.plugin_manager,
            self.on_plugin_changed,
        )
