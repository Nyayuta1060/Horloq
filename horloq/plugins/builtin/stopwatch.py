"""
ストップウォッチプラグイン - 時間計測
"""

import customtkinter as ctk
from horloq.plugins.base import PluginBase
from typing import Optional
from datetime import datetime, timedelta


class StopwatchPlugin(PluginBase):
    """ストップウォッチプラグイン"""
    
    name = "stopwatch"
    version = "1.0.0"
    author = "Horloq Team"
    description = "ストップウォッチ機能を提供します"
    
    def __init__(self, app_context):
        super().__init__(app_context)
        
        self.stopwatch_window: Optional[ctk.CTkToplevel] = None
        self.elapsed_seconds: float = 0.0
        self.is_running: bool = False
        self.stopwatch_job: Optional[str] = None
        self.start_time: Optional[datetime] = None
        self.lap_times: list = []
    
    def initialize(self) -> bool:
        """プラグインを初期化"""
        print(f"[{self.name}] ストップウォッチプラグインを初期化しました")
        return True
    
    def shutdown(self):
        """プラグインを終了"""
        if self.stopwatch_window:
            self.stopwatch_window.destroy()
        print(f"[{self.name}] ストップウォッチプラグインを終了しました")
    
    def create_widget(self, parent: ctk.CTkFrame) -> Optional[ctk.CTkFrame]:
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        # ストップウォッチ起動ボタン
        btn = ctk.CTkButton(
            frame,
            text="⏲️ ストップウォッチを開く",
            command=self._open_stopwatch_window,
            height=40,
        )
        btn.pack(pady=10, padx=10, fill="x")
        
        return frame
    
    def _open_stopwatch_window(self):
        """ストップウォッチウィンドウを開く"""
        if self.stopwatch_window and self.stopwatch_window.winfo_exists():
            self.stopwatch_window.lift()
            self.stopwatch_window.focus()
            return
        
        # 新しいウィンドウを作成
        self.stopwatch_window = ctk.CTkToplevel()
        self.stopwatch_window.title("ストップウォッチ")
        self.stopwatch_window.geometry("350x500")
        
        # タイトル
        title_label = ctk.CTkLabel(
            self.stopwatch_window,
            text="⏲️ ストップウォッチ",
            font=("Arial", 20, "bold"),
        )
        title_label.pack(pady=20)
        
        # 時間表示
        self.time_display = ctk.CTkLabel(
            self.stopwatch_window,
            text="00:00:00.00",
            font=("Arial", 42, "bold"),
        )
        self.time_display.pack(pady=20)
        
        # コントロールボタン
        control_frame = ctk.CTkFrame(self.stopwatch_window)
        control_frame.pack(pady=20, padx=20, fill="x")
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="▶️ 開始",
            command=self._start_stopwatch,
            fg_color="green",
            hover_color="darkgreen",
            height=50,
        )
        self.start_btn.pack(side="left", expand=True, padx=5)
        
        self.lap_btn = ctk.CTkButton(
            control_frame,
            text="📍 ラップ",
            command=self._record_lap,
            state="disabled",
            height=50,
        )
        self.lap_btn.pack(side="left", expand=True, padx=5)
        
        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="🔄 リセット",
            command=self._reset_stopwatch,
            fg_color="gray",
            hover_color="darkgray",
            height=50,
        )
        self.reset_btn.pack(side="left", expand=True, padx=5)
        
        # ラップタイム表示
        lap_label = ctk.CTkLabel(
            self.stopwatch_window,
            text="ラップタイム",
            font=("Arial", 14, "bold"),
        )
        lap_label.pack(pady=(20, 5))
        
        # スクロール可能なラップタイムリスト
        self.lap_frame = ctk.CTkScrollableFrame(
            self.stopwatch_window,
            height=200,
        )
        self.lap_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    def _start_stopwatch(self):
        """ストップウォッチを開始"""
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.now()
            self.start_btn.configure(text="⏸️ 停止", fg_color="orange", hover_color="darkorange")
            self.lap_btn.configure(state="normal")
            self._update_stopwatch()
        else:
            # 一時停止
            self.is_running = False
            self.start_btn.configure(text="▶️ 再開", fg_color="green", hover_color="darkgreen")
            self.lap_btn.configure(state="disabled")
            
            if self.stopwatch_job:
                self.stopwatch_window.after_cancel(self.stopwatch_job)
                self.stopwatch_job = None
    
    def _reset_stopwatch(self):
        """ストップウォッチをリセット"""
        self.is_running = False
        self.elapsed_seconds = 0.0
        self.start_time = None
        self.lap_times = []
        
        if self.stopwatch_job:
            self.stopwatch_window.after_cancel(self.stopwatch_job)
            self.stopwatch_job = None
        
        self.time_display.configure(text="00:00:00.00")
        self.start_btn.configure(text="▶️ 開始", fg_color="green", hover_color="darkgreen")
        self.lap_btn.configure(state="disabled")
        
        # ラップタイムをクリア
        for widget in self.lap_frame.winfo_children():
            widget.destroy()
    
    def _record_lap(self):
        """ラップタイムを記録"""
        if not self.is_running:
            return
        
        lap_number = len(self.lap_times) + 1
        lap_time = self.elapsed_seconds
        self.lap_times.append(lap_time)
        
        # ラップタイムを表示
        hours = int(lap_time // 3600)
        minutes = int((lap_time % 3600) // 60)
        seconds = int(lap_time % 60)
        centiseconds = int((lap_time % 1) * 100)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
        
        # 前回のラップとの差分を計算
        if lap_number > 1:
            diff = lap_time - self.lap_times[-2]
            diff_hours = int(diff // 3600)
            diff_minutes = int((diff % 3600) // 60)
            diff_seconds = int(diff % 60)
            diff_centiseconds = int((diff % 1) * 100)
            diff_str = f"(+{diff_hours:02d}:{diff_minutes:02d}:{diff_seconds:02d}.{diff_centiseconds:02d})"
        else:
            diff_str = ""
        
        lap_label = ctk.CTkLabel(
            self.lap_frame,
            text=f"Lap {lap_number}: {time_str} {diff_str}",
            font=("Arial", 12),
            anchor="w",
        )
        lap_label.pack(fill="x", pady=2)
    
    def _update_stopwatch(self):
        """ストップウォッチを更新"""
        if not self.is_running:
            return
        
        # 経過時間を計算
        if self.start_time:
            delta = datetime.now() - self.start_time
            self.elapsed_seconds = delta.total_seconds()
        
        # 時間表示を更新
        hours = int(self.elapsed_seconds // 3600)
        minutes = int((self.elapsed_seconds % 3600) // 60)
        seconds = int(self.elapsed_seconds % 60)
        centiseconds = int((self.elapsed_seconds % 1) * 100)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
        self.time_display.configure(text=time_str)
        
        # 次の更新をスケジュール（10ms間隔で更新）
        self.stopwatch_job = self.stopwatch_window.after(10, self._update_stopwatch)
    
    def on_enable(self):
        """有効化時の処理"""
        print(f"[{self.name}] ストップウォッチプラグインが有効化されました")
    
    def on_disable(self):
        """無効化時の処理"""
        if self.stopwatch_window:
            self.stopwatch_window.destroy()
        print(f"[{self.name}] ストップウォッチプラグインが無効化されました")
