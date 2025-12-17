"""
タイマープラグイン - カウントダウンタイマー
"""

import customtkinter as ctk
from horloq.plugins.base import PluginBase
from typing import Optional
from datetime import datetime, timedelta


class TimerPlugin(PluginBase):
    """カウントダウンタイマープラグイン"""
    
    name = "timer"
    version = "1.0.0"
    author = "Horloq Team"
    description = "カウントダウンタイマー機能を提供します"
    
    def __init__(self, app_context):
        super().__init__(app_context)
        
        self.timer_window: Optional[ctk.CTkToplevel] = None
        self.remaining_seconds: int = 0
        self.is_running: bool = False
        self.timer_job: Optional[str] = None
    
    def initialize(self) -> bool:
        """プラグインを初期化"""
        print(f"[{self.name}] タイマープラグインを初期化しました")
        return True
    
    def shutdown(self):
        """プラグインを終了"""
        if self.timer_window:
            self.timer_window.destroy()
        print(f"[{self.name}] タイマープラグインを終了しました")
    
    def create_widget(self, parent: ctk.CTkFrame) -> Optional[ctk.CTkFrame]:
        """
        ウィジェットを作成
        
        Note: このプラグインは独立したウィンドウを使用するため、
        親ウィジェットには簡単な起動ボタンのみ表示
        """
        frame = ctk.CTkFrame(parent)
        
        # タイマー起動ボタン
        btn = ctk.CTkButton(
            frame,
            text="⏱️ タイマーを開く",
            command=self._open_timer_window,
            height=40,
        )
        btn.pack(pady=10, padx=10, fill="x")
        
        return frame
    
    def _open_timer_window(self):
        """タイマーウィンドウを開く"""
        if self.timer_window and self.timer_window.winfo_exists():
            # 既に開いている場合は前面に表示
            self.timer_window.lift()
            self.timer_window.focus()
            return
        
        # 新しいウィンドウを作成
        self.timer_window = ctk.CTkToplevel()
        self.timer_window.title("タイマー")
        self.timer_window.geometry("300x400")
        
        # タイトル
        title_label = ctk.CTkLabel(
            self.timer_window,
            text="⏱️ タイマー",
            font=("Arial", 20, "bold"),
        )
        title_label.pack(pady=20)
        
        # 時間表示
        self.time_display = ctk.CTkLabel(
            self.timer_window,
            text="00:00:00",
            font=("Arial", 48, "bold"),
        )
        self.time_display.pack(pady=20)
        
        # 時間設定フレーム
        time_frame = ctk.CTkFrame(self.timer_window)
        time_frame.pack(pady=10, padx=20, fill="x")
        
        # 時間入力
        input_frame = ctk.CTkFrame(time_frame)
        input_frame.pack(pady=10)
        
        ctk.CTkLabel(input_frame, text="時:").grid(row=0, column=0, padx=5)
        self.hours_entry = ctk.CTkEntry(input_frame, width=50)
        self.hours_entry.insert(0, "0")
        self.hours_entry.grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(input_frame, text="分:").grid(row=0, column=2, padx=5)
        self.minutes_entry = ctk.CTkEntry(input_frame, width=50)
        self.minutes_entry.insert(0, "5")
        self.minutes_entry.grid(row=0, column=3, padx=5)
        
        ctk.CTkLabel(input_frame, text="秒:").grid(row=0, column=4, padx=5)
        self.seconds_entry = ctk.CTkEntry(input_frame, width=50)
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.grid(row=0, column=5, padx=5)
        
        # プリセットボタン
        preset_frame = ctk.CTkFrame(time_frame)
        preset_frame.pack(pady=10, fill="x")
        
        presets = [
            ("1分", 60),
            ("3分", 180),
            ("5分", 300),
            ("10分", 600),
            ("30分", 1800),
        ]
        
        for i, (label, seconds) in enumerate(presets):
            btn = ctk.CTkButton(
                preset_frame,
                text=label,
                command=lambda s=seconds: self._set_preset(s),
                width=50,
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
        
        # コントロールボタン
        control_frame = ctk.CTkFrame(self.timer_window)
        control_frame.pack(pady=20, padx=20, fill="x")
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="▶️ 開始",
            command=self._start_timer,
            fg_color="green",
            hover_color="darkgreen",
        )
        self.start_btn.pack(side="left", expand=True, padx=5)
        
        self.pause_btn = ctk.CTkButton(
            control_frame,
            text="⏸️ 一時停止",
            command=self._pause_timer,
            state="disabled",
        )
        self.pause_btn.pack(side="left", expand=True, padx=5)
        
        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="🔄 リセット",
            command=self._reset_timer,
            fg_color="gray",
            hover_color="darkgray",
        )
        self.reset_btn.pack(side="left", expand=True, padx=5)
    
    def _set_preset(self, seconds: int):
        """プリセット時間を設定"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        self.hours_entry.delete(0, "end")
        self.hours_entry.insert(0, str(hours))
        
        self.minutes_entry.delete(0, "end")
        self.minutes_entry.insert(0, str(minutes))
        
        self.seconds_entry.delete(0, "end")
        self.seconds_entry.insert(0, str(secs))
    
    def _start_timer(self):
        """タイマーを開始"""
        if not self.is_running:
            # 入力から秒数を計算
            try:
                hours = int(self.hours_entry.get() or 0)
                minutes = int(self.minutes_entry.get() or 0)
                seconds = int(self.seconds_entry.get() or 0)
                
                self.remaining_seconds = hours * 3600 + minutes * 60 + seconds
                
                if self.remaining_seconds <= 0:
                    return
                
                self.is_running = True
                self.start_btn.configure(state="disabled")
                self.pause_btn.configure(state="normal")
                
                self._update_timer()
                
            except ValueError:
                print("無効な時間入力です")
    
    def _pause_timer(self):
        """タイマーを一時停止"""
        if self.is_running:
            self.is_running = False
            self.start_btn.configure(state="normal", text="▶️ 再開")
            self.pause_btn.configure(state="disabled")
            
            if self.timer_job:
                self.timer_window.after_cancel(self.timer_job)
                self.timer_job = None
    
    def _reset_timer(self):
        """タイマーをリセット"""
        self.is_running = False
        self.remaining_seconds = 0
        
        if self.timer_job:
            self.timer_window.after_cancel(self.timer_job)
            self.timer_job = None
        
        self.time_display.configure(text="00:00:00")
        self.start_btn.configure(state="normal", text="▶️ 開始")
        self.pause_btn.configure(state="disabled")
    
    def _update_timer(self):
        """タイマーを更新"""
        if not self.is_running or self.remaining_seconds <= 0:
            self._on_timer_finished()
            return
        
        # 時間表示を更新
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_display.configure(text=time_str)
        
        # 1秒減らす
        self.remaining_seconds -= 1
        
        # 次の更新をスケジュール
        self.timer_job = self.timer_window.after(1000, self._update_timer)
    
    def _on_timer_finished(self):
        """タイマー終了時の処理"""
        self.is_running = False
        self.time_display.configure(text="00:00:00", text_color="red")
        self.start_btn.configure(state="normal", text="▶️ 開始")
        self.pause_btn.configure(state="disabled")
        
        # 通知（今後実装）
        print("⏰ タイマーが終了しました！")
        
        # 一定時間後に色を元に戻す
        self.timer_window.after(3000, lambda: self.time_display.configure(text_color="white"))
    
    def on_enable(self):
        """有効化時の処理"""
        print(f"[{self.name}] タイマープラグインが有効化されました")
    
    def on_disable(self):
        """無効化時の処理"""
        if self.timer_window:
            self.timer_window.destroy()
        print(f"[{self.name}] タイマープラグインが無効化されました")
