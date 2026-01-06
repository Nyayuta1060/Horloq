"""
コンテキストメニュー（右クリックメニュー）
"""

import customtkinter as ctk
from typing import Callable, List, Tuple, Optional


class ContextMenu:
    """コンテキストメニュー"""
    
    def __init__(self, parent):
        """
        初期化
        
        Args:
            parent: 親ウィジェット
        """
        self.parent = parent
        self.menu = None
    
    def show(self, event, items: List[Tuple[str, Callable]]):
        """
        メニューを表示
        
        Args:
            event: マウスイベント
            items: メニュー項目のリスト [(ラベル, コールバック), ...]
        """
        # 既存のメニューがあれば破棄
        if self.menu:
            self.menu.destroy()
        
        # 新しいメニューを作成
        self.menu = ctk.CTkToplevel(self.parent)
        self.menu.withdraw()  # 一時的に非表示
        
        # ウィンドウ装飾を削除
        self.menu.overrideredirect(True)
        
        # メニューの背景色とボーダーを設定
        self.menu.configure(fg_color="#1e1e1e")
        
        # メニューコンテナ（ボーダー用）
        menu_container = ctk.CTkFrame(
            self.menu,
            fg_color="#1e1e1e",
            border_color="#3e3e42",
            border_width=1,
        )
        menu_container.pack(fill="both", expand=True)
        
        # メニュー項目を追加
        for label, callback in items:
            if label == "---":
                # セパレータ
                separator = ctk.CTkFrame(
                    menu_container, 
                    height=1, 
                    fg_color="#3e3e42"
                )
                separator.pack(fill="x", padx=8, pady=4)
            else:
                btn = ctk.CTkButton(
                    menu_container,
                    text=label,
                    command=lambda cb=callback: self._on_item_click(cb),
                    fg_color="transparent",
                    hover_color="#2a2a2a",
                    text_color="#cccccc",
                    anchor="w",
                    height=32,
                    font=("Segoe UI", 13),
                    corner_radius=4,
                )
                btn.pack(fill="x", padx=4, pady=2)
        
        # メニューの位置を設定
        self.menu.geometry(f"+{event.x_root}+{event.y_root}")
        self.menu.deiconify()  # 表示
        
        # メニュー外をクリックしたら閉じる
        self.menu.bind("<FocusOut>", lambda e: self._close_menu())
        self.menu.focus_set()
    
    def _on_item_click(self, callback: Callable):
        """
        メニュー項目がクリックされた時の処理
        
        Args:
            callback: コールバック関数
        """
        self._close_menu()
        if callback:
            callback()
    
    def _close_menu(self):
        """メニューを閉じる"""
        if self.menu:
            self.menu.destroy()
            self.menu = None


class SystemTrayMenu:
    """システムトレイメニュー（将来の実装用）"""
    
    def __init__(self, app):
        """
        初期化
        
        Args:
            app: HorloqAppインスタンス
        """
        self.app = app
        # TODO: pystray などを使用してシステムトレイを実装
    
    def create(self):
        """システムトレイアイコンを作成"""
        # TODO: 実装
        pass
    
    def remove(self):
        """システムトレイアイコンを削除"""
        # TODO: 実装
        pass
