"""
時計表示UIコンポーネント
"""

import customtkinter as ctk
from datetime import datetime
from typing import Optional
import pytz


class DigitalClock(ctk.CTkFrame):
    """デジタル時計ウィジェット"""
    
    def __init__(
        self,
        master,
        timezone: str = "Asia/Tokyo",
        format_24h: bool = True,
        show_seconds: bool = True,
        show_date: bool = True,
        date_format: str = "%Y/%m/%d",
        font_size: int = 48,
        **kwargs
    ):
        """
        初期化
        
        Args:
            master: 親ウィジェット
            timezone: タイムゾーン
            format_24h: 24時間形式かどうか
            show_seconds: 秒を表示するかどうか
            show_date: 日付を表示するかどうか
            date_format: 日付フォーマット
            font_size: フォントサイズ
            **kwargs: その他のフレームオプション
        """
        super().__init__(master, **kwargs)
        
        self.timezone = pytz.timezone(timezone)
        self.format_24h = format_24h
        self.show_seconds = show_seconds
        self.show_date = show_date
        self.date_format = date_format
        self.font_size = font_size
        
        self._update_job: Optional[str] = None
        
        self._setup_ui()
        self._start_update()
    
    def _setup_ui(self):
        """UIをセットアップ"""
        # 時刻ラベル
        self.time_label = ctk.CTkLabel(
            self,
            text="00:00:00",
            font=("Arial", self.font_size, "bold"),
        )
        self.time_label.pack(pady=10)
        
        # 日付ラベル
        if self.show_date:
            self.date_label = ctk.CTkLabel(
                self,
                text="2024/01/01",
                font=("Arial", self.font_size // 3),
            )
            self.date_label.pack()
    
    def apply_theme(self, theme):
        """
        テーマを適用
        
        Args:
            theme: Themeオブジェクト
        """
        # 背景色を透明に設定
        self.configure(fg_color="transparent")
        
        # 時刻ラベルの色を設定
        self.time_label.configure(text_color=theme.fg)
        
        # 日付ラベルの色を設定
        if self.show_date and hasattr(self, 'date_label'):
            self.date_label.configure(text_color=theme.fg_secondary or theme.fg)
    
    def _update_time(self):
        """時刻を更新"""
        now = datetime.now(self.timezone)
        
        # 時刻フォーマット
        if self.format_24h:
            time_format = "%H:%M:%S" if self.show_seconds else "%H:%M"
        else:
            time_format = "%I:%M:%S %p" if self.show_seconds else "%I:%M %p"
        
        time_str = now.strftime(time_format)
        self.time_label.configure(text=time_str)
        
        # 日付更新
        if self.show_date:
            date_str = now.strftime(self.date_format)
            self.date_label.configure(text=date_str)
    
    def _start_update(self):
        """更新を開始"""
        self._update_time()
        # 1秒ごとに更新
        self._update_job = self.after(1000, self._start_update)
    
    def stop_update(self):
        """更新を停止"""
        if self._update_job is not None:
            self.after_cancel(self._update_job)
            self._update_job = None
    
    def set_timezone(self, timezone: str):
        """
        タイムゾーンを設定
        
        Args:
            timezone: タイムゾーン文字列
        """
        self.timezone = pytz.timezone(timezone)
        self._update_time()
    
    def set_format(self, format_24h: bool):
        """
        時刻フォーマットを設定
        
        Args:
            format_24h: 24時間形式かどうか
        """
        self.format_24h = format_24h
        self._update_time()
    
    def destroy(self):
        """ウィジェットを破棄"""
        self.stop_update()
        super().destroy()
