"""
サンプルプラグイン - Hello World
"""

import customtkinter as ctk
from horloq.plugins.base import PluginBase


class HelloPlugin(PluginBase):
    """Hello Worldプラグイン"""
    
    name = "hello"
    version = "0.1.0"
    author = "Horloq Team"
    description = "シンプルなHello Worldプラグイン"
    
    def initialize(self) -> bool:
        """プラグインを初期化"""
        print(f"[{self.name}] プラグインを初期化しました")
        return True
    
    def shutdown(self):
        """プラグインを終了"""
        print(f"[{self.name}] プラグインを終了しました")
    
    def create_widget(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        label = ctk.CTkLabel(
            frame,
            text="Hello, Horloq!",
            font=("Arial", 16),
        )
        label.pack(pady=10)
        
        return frame
    
    def on_enable(self):
        """有効化時の処理"""
        print(f"[{self.name}] プラグインが有効化されました")
    
    def on_disable(self):
        """無効化時の処理"""
        print(f"[{self.name}] プラグインが無効化されました")
