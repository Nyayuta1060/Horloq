"""
プラグイン管理UI
"""

import customtkinter as ctk
from typing import Callable, Optional
from pathlib import Path
from ..plugins.manager import PluginManager
from ..plugins.installer import PluginInstaller


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
        
        # プラグインインストーラーを初期化
        from ..core.config import ConfigManager
        config = ConfigManager()
        plugin_dir = config.config_path.parent / "plugins"
        self.installer = PluginInstaller(plugin_dir)
        
        # 更新情報をキャッシュ
        self.available_updates = {}
        self._fetch_updates()
        
        self._setup_window()
        self._create_widgets()
    
    def _setup_window(self):
        """ウィンドウをセットアップ"""
        self.title("プラグイン管理")
        self.geometry("650x650")
        self.minsize(600, 500)
        
        # モーダルウィンドウとして表示
        self.transient(self.master)
        # ウィンドウが表示された後にgrab_setを呼ぶ
        self.after(10, self.grab_set)
        
        # ウィンドウを閉じるときの処理を設定
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """ウィジェットを作成"""
        # タイトル
        title_label = ctk.CTkLabel(
            self,
            text="プラグイン管理",
            font=("Arial", 20, "bold"),
        )
        title_label.pack(pady=20)
        
        # 説明
        desc_label = ctk.CTkLabel(
            self,
            text="利用可能なプラグインの一覧です。チェックボックスで有効/無効を切り替えできます。",
            font=("Arial", 12),
        )
        desc_label.pack(pady=(0, 10))
        
        # インストールボタン
        install_frame = ctk.CTkFrame(self)
        install_frame.pack(pady=10, padx=20, fill="x")
        
        install_label = ctk.CTkLabel(
            install_frame,
            text="新しいプラグインをインストール:",
            font=("Arial", 12, "bold"),
        )
        install_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # ボタンコンテナ
        button_container = ctk.CTkFrame(install_frame, fg_color="transparent")
        button_container.pack(fill="x", padx=10, pady=(5, 10))
        
        # 公式プラグイン
        official_btn = ctk.CTkButton(
            button_container,
            text="🏆 公式プラグイン",
            command=self._show_official_plugins,
            fg_color="#6f42c1",
            hover_color="#5a32a3",
            width=150,
            height=35,
        )
        official_btn.pack(side="left", padx=5)
        
        # カタログから選択
        browse_btn = ctk.CTkButton(
            button_container,
            text="カタログから選択",
            command=self._show_catalog_dialog,
            fg_color="#28a745",
            hover_color="#218838",
            width=150,
            height=35,
        )
        browse_btn.pack(side="left", padx=5)
        
        # GitHubから直接
        install_btn = ctk.CTkButton(
            button_container,
            text="🔗 GitHubから直接",
            command=self._show_install_dialog,
            fg_color="#007acc",
            hover_color="#0098ff",
            width=150,
            height=35,
        )
        install_btn.pack(side="left", padx=5)
        
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
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # 再読み込みボタン
        reload_btn = ctk.CTkButton(
            button_frame,
            text="再読み込み",
            command=self._reload_plugins,
            fg_color="gray",
            hover_color="darkgray",
            width=120,
            height=35,
        )
        reload_btn.pack(side="right", padx=5)
        
        # 閉じるボタン
        close_btn = ctk.CTkButton(
            button_frame,
            text="閉じる",
            command=self._on_closing,
            width=120,
            height=35,
        )
        close_btn.pack(side="right", padx=5)
    
    def _show_install_dialog(self):
        """インストールダイアログを表示"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("プラグインをインストール")
        dialog.geometry("500x250")
        dialog.transient(self)
        dialog.update_idletasks()
        dialog.after(10, dialog.grab_set)
        
        # タイトル
        title = ctk.CTkLabel(
            dialog,
            text="GitHubリポジトリからインストール",
            font=("Arial", 16, "bold"),
        )
        title.pack(pady=20)
        
        # 説明
        desc = ctk.CTkLabel(
            dialog,
            text="GitHubのリポジトリURLまたは 'ユーザー名/リポジトリ名' を入力してください",
            font=("Arial", 12),
        )
        desc.pack(pady=(0, 10))
        
        # 入力フレーム
        input_frame = ctk.CTkFrame(dialog)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        url_label = ctk.CTkLabel(input_frame, text="URL:", font=("Arial", 12))
        url_label.pack(side="left", padx=10)
        
        url_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="例: username/horloq-plugin-example",
            width=300,
        )
        url_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        # ステータスラベル
        status_label = ctk.CTkLabel(
            dialog,
            text="",
            font=("Arial", 11),
        )
        status_label.pack(pady=10)
        
        # ボタンフレーム
        btn_frame = ctk.CTkFrame(dialog)
        btn_frame.pack(pady=20, padx=20, fill="x")
        
        def do_install():
            url = url_entry.get().strip()
            if not url:
                status_label.configure(text="URLを入力してください", text_color="red")
                return
            
            status_label.configure(text="インストール中...", text_color="white")
            dialog.update()
            
            success, message = self.installer.install_from_github(url)
            
            if success:
                status_label.configure(text=f"{message}\n\n2秒後にウィンドウを閉じます...", text_color="green")
                dialog.after(2000, lambda: [dialog.destroy(), self._reload_plugins()])
            else:
                status_label.configure(text=message, text_color="red")
        
        install_btn = ctk.CTkButton(
            btn_frame,
            text="インストール",
            command=do_install,
            fg_color="#007acc",
            hover_color="#0098ff",
        )
        install_btn.pack(side="right", padx=5)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="キャンセル",
            command=dialog.destroy,
        )
        cancel_btn.pack(side="right", padx=5)
    
    def _show_official_plugins(self):
        """公式プラグインダイアログを表示"""
        # 公式リポジトリを自動読み込み
        self._show_catalog_dialog_internal("Nyayuta1060/Horloq-Plugins", "公式プラグイン")
    
    def _show_catalog_dialog(self):
        """カタログダイアログを表示"""
        self._show_catalog_dialog_internal(None, "プラグインカタログから選択")
    
    def _show_catalog_dialog_internal(self, default_repo: Optional[str], title_text: str):
        """カタログダイアログを表示（内部実装）"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("プラグインカタログ")
        dialog.geometry("600x500")
        dialog.transient(self)
        dialog.update_idletasks()
        dialog.after(10, dialog.grab_set)
        
        # タイトル
        title = ctk.CTkLabel(
            dialog,
            text=title_text,
            font=("Arial", 16, "bold"),
        )
        title.pack(pady=20)
        
        # リポジトリ入力（公式プラグインの場合は非表示）
        repo_frame = ctk.CTkFrame(dialog)
        if default_repo:
            # 公式プラグインの場合は入力欄を非表示
            pass
        else:
            repo_frame.pack(pady=10, padx=20, fill="x")
            
            repo_label = ctk.CTkLabel(repo_frame, text="リポジトリ:", font=("Arial", 12))
            repo_label.pack(side="left", padx=10)
            
            repo_entry = ctk.CTkEntry(
                repo_frame,
                placeholder_text="例: username/horloq-plugins",
                width=300,
            )
            repo_entry.pack(side="left", fill="x", expand=True, padx=10)
            
            load_btn = ctk.CTkButton(
                repo_frame,
                text="読み込み",
                command=lambda: load_catalog(),
                width=80,
            )
            load_btn.pack(side="right", padx=10)
        
        # ステータスラベル
        initial_status = "カタログを読み込んでいます..." if default_repo else "リポジトリURLを入力してカタログを読み込んでください"
        status_label = ctk.CTkLabel(
            dialog,
            text=initial_status,
            font=("Arial", 11),
        )
        status_label.pack(pady=5)
        
        # プラグインリスト
        list_frame = ctk.CTkScrollableFrame(dialog, height=250)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        def load_catalog(repo_url=None):
            if repo_url is None:
                if default_repo:
                    repo_url = default_repo
                else:
                    repo_url = repo_entry.get().strip()
            
            if not repo_url:
                status_label.configure(text="リポジトリURLを入力してください", text_color="red")
                return
            
            status_label.configure(text="カタログを読み込んでいます...", text_color="white")
            dialog.update()
            
            success, plugins = self.installer.fetch_plugin_catalog(repo_url)
            
            if not success or not plugins:
                status_label.configure(text="カタログの読み込みに失敗しました", text_color="red")
                return
            
            # 既存のリストをクリア
            for widget in list_frame.winfo_children():
                widget.destroy()
            
            status_label.configure(text=f"{len(plugins)} 個のプラグインが見つかりました", text_color="green")
            
            # プラグインカードを表示
            for plugin in plugins:
                create_plugin_card(list_frame, plugin)
        
        # 公式プラグインの場合は自動的に読み込む
        if default_repo:
            dialog.after(100, lambda: load_catalog(default_repo))
        
        def create_plugin_card(parent, plugin):
            card = ctk.CTkFrame(parent)
            card.pack(fill="x", pady=5, padx=5)
            
            # プラグイン情報
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
            
            name = plugin.get("name", "不明")
            desc = plugin.get("description", "説明なし")
            version = plugin.get("version", "")
            
            # インストール済みかチェック
            is_installed = self.installer.get_plugin_info(name) is not None
            
            # タイトル（インストール済みの場合はバッジを追加）
            title_text = f"{name}"
            if is_installed:
                title_text += " [インストール済み]"
            
            name_label = ctk.CTkLabel(
                info_frame,
                text=title_text,
                font=("Arial", 14, "bold"),
                anchor="w",
                text_color="#4caf50" if is_installed else "white",
            )
            name_label.pack(anchor="w")
            
            # 説明（バージョン情報を追加）
            desc_text = desc
            if version:
                desc_text += f" (v{version})"
            
            desc_label = ctk.CTkLabel(
                info_frame,
                text=desc_text,
                font=("Arial", 11),
                text_color="gray70",
                anchor="w",
            )
            desc_label.pack(anchor="w")
            
            # インストール/更新ボタン
            def install_from_catalog():
                repo = plugin.get("repository")
                path = plugin.get("path", name)
                install_url = f"{repo}:{path}"
                
                status_label.configure(text=f"{name} をインストール中...", text_color="white")
                dialog.update()
                
                success, message = self.installer.install_from_github(install_url)
                
                if success:
                    status_label.configure(text=message, text_color="green")
                    # インストールボタンを無効化
                    install_btn.configure(state="disabled", text="インストール済み", fg_color="gray")
                    name_label.configure(text=f"{name} [インストール済み]", text_color="#4caf50")
                else:
                    status_label.configure(text=message, text_color="red")
            
            # ボタンの状態を設定
            if is_installed:
                install_btn = ctk.CTkButton(
                    card,
                    text="インストール済み",
                    command=None,
                    state="disabled",
                    fg_color="gray",
                    width=120,
                    height=32,
                )
            else:
                install_btn = ctk.CTkButton(
                    card,
                    text="インストール",
                    command=install_from_catalog,
                    fg_color="#007acc",
                    hover_color="#0098ff",
                    width=120,
                    height=32,
                )
            install_btn.pack(side="right", padx=15)
        
        # 閉じるボタン
        close_btn = ctk.CTkButton(
            dialog,
            text="閉じる",
            command=lambda: [dialog.destroy(), self._reload_plugins()],
        )
        close_btn.pack(pady=20)
    
    def _fetch_updates(self):
        """プラグインの更新情報を取得"""
        try:
            success, updates = self.installer.check_for_updates()
            if success and updates:
                # プラグイン名をキーにした辞書に変換
                self.available_updates = {u['name']: u for u in updates}
        except Exception as e:
            print(f"更新情報の取得に失敗: {e}")
            self.available_updates = {}
    
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
        
        # プラグインの詳細情報を取得（plugin.yamlから直接読み込む）
        plugin_info = self.installer.get_plugin_info(plugin_name)
        if plugin_info:
            description = plugin_info.get("description", "説明なし")
            version = plugin_info.get("version", "不明")
            author = plugin_info.get("author", "不明")
            desc_text = f"{description} (v{version} by {author})"
        else:
            # アクティブなプラグインから取得を試みる（フォールバック）
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
        
        # 更新情報があれば表示
        if plugin_name in self.available_updates:
            update_info = self.available_updates[plugin_name]
            update_label = ctk.CTkLabel(
                info_frame,
                text=f"🔔 更新あり: v{update_info['current_version']} → v{update_info['latest_version']}",
                font=("Arial", 10, "bold"),
                text_color="#4A90E2",
                anchor="w",
            )
            update_label.pack(anchor="w", pady=(2, 0))
            
            # 更新ボタン
            update_btn = ctk.CTkButton(
                item_frame,
                text="更新",
                command=lambda: self._update_plugin(plugin_name),
                fg_color="#4A90E2",
                hover_color="#357ABD",
                width=60,
            )
            update_btn.pack(side="right", padx=5)
        
        # アンインストールボタンを表示（すべてのプラグインで表示）
        if plugin_info:
            uninstall_btn = ctk.CTkButton(
                item_frame,
                text="削除",
                command=lambda: self._uninstall_plugin(plugin_name),
                fg_color="#d32f2f",
                hover_color="#b71c1c",
                width=60,
            )
            uninstall_btn.pack(side="right", padx=10)
    
    def _uninstall_plugin(self, plugin_name: str):
        """プラグインをアンインストール"""
        # 確認ダイアログ
        dialog = ctk.CTkToplevel(self)
        dialog.title("確認")
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.update_idletasks()
        dialog.after(10, dialog.grab_set)
        
        message = ctk.CTkLabel(
            dialog,
            text=f"プラグイン '{plugin_name}' を削除しますか？",
            font=("Arial", 14),
        )
        message.pack(pady=30)
        
        btn_frame = ctk.CTkFrame(dialog)
        btn_frame.pack(pady=10)
        
        def do_uninstall():
            # 有効な場合は先に無効化
            if plugin_name in self.plugin_manager.list_active_plugins():
                self.plugin_manager.unload_plugin(plugin_name)
            
            success, msg = self.installer.uninstall(plugin_name)
            dialog.destroy()
            
            if success:
                self._reload_plugins()
            else:
                # エラーダイアログ
                error_dialog = ctk.CTkToplevel(self)
                error_dialog.title("エラー")
                error_dialog.geometry("400x120")
                error_msg = ctk.CTkLabel(error_dialog, text=msg, font=("Arial", 12))
                error_msg.pack(pady=30)
                ok_btn = ctk.CTkButton(error_dialog, text="OK", command=error_dialog.destroy)
                ok_btn.pack(pady=10)
        
        yes_btn = ctk.CTkButton(
            btn_frame,
            text="はい",
            command=do_uninstall,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
        )
        yes_btn.pack(side="left", padx=10)
        
        no_btn = ctk.CTkButton(
            btn_frame,
            text="いいえ",
            command=dialog.destroy,
        )
        no_btn.pack(side="left", padx=10)
    
    def _update_plugin(self, plugin_name: str):
        """プラグインを更新"""
        if plugin_name not in self.available_updates:
            return
        
        update_info = self.available_updates[plugin_name]
        
        # 確認ダイアログ
        dialog = ctk.CTkToplevel(self)
        dialog.title("プラグイン更新")
        dialog.geometry("450x200")
        dialog.transient(self)
        dialog.update_idletasks()
        dialog.after(10, dialog.grab_set)
        
        message = ctk.CTkLabel(
            dialog,
            text=f"'{plugin_name}' を更新しますか？\n\n"
                 f"現在のバージョン: v{update_info['current_version']}\n"
                 f"最新バージョン: v{update_info['latest_version']}",
            font=("Arial", 13),
            justify="center",
        )
        message.pack(pady=30)
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        def do_update():
            dialog.destroy()
            
            # プラグインを無効化
            was_enabled = plugin_name in self.plugin_manager.list_enabled_plugins()
            if was_enabled:
                self.plugin_manager.unload_plugin(plugin_name)
            
            # 既存のプラグインをアンインストール
            success, msg = self.installer.uninstall(plugin_name)
            if not success:
                error_dialog = ctk.CTkToplevel(self)
                error_dialog.title("エラー")
                error_dialog.geometry("400x120")
                error_msg = ctk.CTkLabel(error_dialog, text=f"アンインストールに失敗: {msg}", font=("Arial", 12))
                error_msg.pack(pady=30)
                ok_btn = ctk.CTkButton(error_dialog, text="OK", command=error_dialog.destroy)
                ok_btn.pack(pady=10)
                return
            
            # 新しいバージョンをインストール
            repo = update_info.get('repository', 'Nyayuta1060/Horloq-Plugins')
            success, msg = self.installer.install_from_github(repo, plugin_name)
            
            if success:
                # 成功ダイアログ
                success_dialog = ctk.CTkToplevel(self)
                success_dialog.title("成功")
                success_dialog.geometry("400x120")
                success_msg = ctk.CTkLabel(
                    success_dialog,
                    text=f"'{plugin_name}' を v{update_info['latest_version']} に更新しました",
                    font=("Arial", 12)
                )
                success_msg.pack(pady=30)
                ok_btn = ctk.CTkButton(success_dialog, text="OK", command=success_dialog.destroy)
                ok_btn.pack(pady=10)
                
                # 以前有効だった場合は再度有効化
                if was_enabled:
                    self.plugin_manager.load_plugin(plugin_name)
                
                # リストを再読み込み
                self._reload_plugins()
            else:
                # エラーダイアログ
                error_dialog = ctk.CTkToplevel(self)
                error_dialog.title("エラー")
                error_dialog.geometry("400x150")
                error_msg = ctk.CTkLabel(error_dialog, text=f"更新に失敗:\n{msg}", font=("Arial", 12))
                error_msg.pack(pady=30)
                ok_btn = ctk.CTkButton(error_dialog, text="OK", command=error_dialog.destroy)
                ok_btn.pack(pady=10)
        
        update_btn = ctk.CTkButton(
            btn_frame,
            text="更新",
            command=do_update,
            fg_color="#4A90E2",
            hover_color="#357ABD",
        )
        update_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="キャンセル",
            command=dialog.destroy,
        )
        cancel_btn.pack(side="left", padx=10)
    
    def _toggle_plugin(self, plugin_name: str, enable: bool):
        """プラグインの有効/無効を切り替え"""
        try:
            if enable:
                success = self.plugin_manager.load_plugin(plugin_name)
                if success:
                    print(f"プラグイン '{plugin_name}' を有効化しました")
                else:
                    print(f"プラグイン '{plugin_name}' の有効化に失敗しました")
            else:
                success = self.plugin_manager.unload_plugin(plugin_name)
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
        # プラグインを再検出
        self.plugin_manager.discover_plugins()
        
        # ウィンドウを閉じて再度開く
        self.destroy()
        new_window = PluginManagerWindow(
            self.master,
            self.plugin_manager,
            self.on_plugin_changed,
        )
        new_window.focus()
    
    def _on_closing(self):
        """ウィンドウを閉じる"""
        if self.on_plugin_changed:
            self.on_plugin_changed()
        self.destroy()
