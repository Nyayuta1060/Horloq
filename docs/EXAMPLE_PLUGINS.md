# サンプルプラグイン集

このドキュメントでは、Horloq用のサンプルプラグインの実装例を紹介します。
これらをモノレポとして公開することで、ユーザーは必要なプラグインだけを選択してインストールできます。

## モノレポの構成例

```
horloq-official-plugins/
├── plugins.yaml           # 自動生成されるカタログ
├── generate_catalog.py    # カタログ生成スクリプト
├── hello/
│   ├── plugin.yaml
│   └── __init__.py
├── timer/
│   ├── plugin.yaml
│   └── __init__.py
└── stopwatch/
    ├── plugin.yaml
    └── __init__.py
```

## plugins.yaml（自動生成）

**⚠️ 重要**: `plugins.yaml`は手動で編集せず、`generate_catalog.py`で自動生成してください。

```yaml
repository: Nyayuta1060/horloq-official-plugins
plugins:
  - name: hello
    path: hello
    description: シンプルなHello Worldプラグイン
    version: 1.0.0
    author: Nyayuta1060
  
  - name: timer
    path: timer
    description: カウントダウンタイマー（プリセット機能付き）
    version: 1.0.0
    author: Nyayuta1060
  
  - name: stopwatch
    path: stopwatch
    description: 精密時間計測（ラップタイム機能付き）
    version: 1.0.0
    author: Nyayuta1060
```

## 1. Hello プラグイン

### hello/plugin.yaml
```yaml
name: hello
version: 1.0.0
author: Nyayuta1060
description: シンプルなHello Worldプラグイン
min_horloq_version: 0.1.0
```

### hello/__init__.py
```python
"""
Helloプラグイン - サンプルプラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk


class HelloPlugin(PluginBase):
    """シンプルなHello Worldプラグイン"""
    
    def __init__(self, app_context):
        # plugin.yamlから自動的にメタデータを読み込みます
        super().__init__(app_context)
    
    def initialize(self) -> bool:
        """初期化"""
        print("Hello plugin initialized!")
        return True
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        label = ctk.CTkLabel(
            frame,
            text="👋 Hello, Horloq!",
            font=("Arial", 16),
        )
        label.pack(pady=10, padx=20)
        
        return frame
    
    def shutdown(self):
        """終了処理"""
        print("Hello plugin shutdown")


# プラグインクラスをエクスポート
Plugin = HelloPlugin
```

## 2. Timer プラグイン

### timer/plugin.yaml
```yaml
name: timer
version: 1.0.0
author: Nyayuta1060
description: カウントダウンタイマー（プリセット機能付き）
min_horloq_version: 0.1.0
```

### timer/__init__.py
```python
"""
タイマープラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk
from datetime import timedelta


class TimerPlugin(PluginBase):
    """カウントダウンタイマープラグイン"""
    
    def __init__(self, app_context):
        # plugin.yamlから自動的にメタデータを読み込みます
        super().__init__(app_context)
        self.timer_window = None
        self.remaining_time = 0
        self.is_running = False
        self.after_id = None
    
    def initialize(self) -> bool:
        """初期化"""
        return True
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        button = ctk.CTkButton(
            frame,
            text="⏱️ タイマーを開く",
            command=self._open_timer_window,
        )
        button.pack(pady=10, padx=20)
        
        return frame
    
    def _open_timer_window(self):
        """タイマーウィンドウを開く"""
        if self.timer_window and self.timer_window.winfo_exists():
            self.timer_window.focus()
            return
        
        self.timer_window = ctk.CTkToplevel()
        self.timer_window.title("タイマー")
        self.timer_window.geometry("300x400")
        
        # タイマー表示
        self.time_label = ctk.CTkLabel(
            self.timer_window,
            text="00:00:00",
            font=("Arial", 48, "bold"),
        )
        self.time_label.pack(pady=30)
        
        # プリセットボタン
        preset_frame = ctk.CTkFrame(self.timer_window)
        preset_frame.pack(pady=10)
        
        presets = [
            ("1分", 60),
            ("3分", 180),
            ("5分", 300),
            ("10分", 600),
        ]
        
        for label, seconds in presets:
            btn = ctk.CTkButton(
                preset_frame,
                text=label,
                command=lambda s=seconds: self._set_timer(s),
                width=60,
            )
            btn.pack(side="left", padx=5)
        
        # コントロールボタン
        control_frame = ctk.CTkFrame(self.timer_window)
        control_frame.pack(pady=20)
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="開始",
            command=self._start_timer,
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="停止",
            command=self._stop_timer,
            state="disabled",
        )
        self.stop_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="リセット",
            command=self._reset_timer,
        )
        self.reset_btn.pack(side="left", padx=5)
    
    def _set_timer(self, seconds: int):
        """タイマーを設定"""
        self.remaining_time = seconds
        self._update_display()
    
    def _start_timer(self):
        """タイマーを開始"""
        if self.remaining_time <= 0:
            return
        
        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self._tick()
    
    def _stop_timer(self):
        """タイマーを停止"""
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if self.after_id:
            self.timer_window.after_cancel(self.after_id)
    
    def _reset_timer(self):
        """タイマーをリセット"""
        self._stop_timer()
        self.remaining_time = 0
        self._update_display()
    
    def _tick(self):
        """タイマーの1秒ごとの更新"""
        if not self.is_running:
            return
        
        self.remaining_time -= 1
        self._update_display()
        
        if self.remaining_time <= 0:
            self._timer_finished()
        else:
            self.after_id = self.timer_window.after(1000, self._tick)
    
    def _timer_finished(self):
        """タイマー終了"""
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.time_label.configure(text="終了！", text_color="green")
    
    def _update_display(self):
        """表示を更新"""
        td = timedelta(seconds=self.remaining_time)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = td.seconds % 60
        self.time_label.configure(
            text=f"{hours:02d}:{minutes:02d}:{seconds:02d}",
            text_color="white",
        )
    
    def shutdown(self):
        """終了処理"""
        self._stop_timer()
        if self.timer_window and self.timer_window.winfo_exists():
            self.timer_window.destroy()


# プラグインクラスをエクスポート
Plugin = TimerPlugin
```

## 3. Stopwatch プラグイン

### stopwatch/plugin.yaml
```yaml
name: stopwatch
version: 1.0.0
author: Nyayuta1060
description: 精密時間計測（ラップタイム機能付き）
min_horloq_version: 0.1.0
```

### stopwatch/__init__.py
```python
"""
ストップウォッチプラグイン
"""

from horloq.plugins.base import PluginBase
import customtkinter as ctk
import time


class StopwatchPlugin(PluginBase):
    """ストップウォッチプラグイン"""
    
    def __init__(self, app_context):
        # plugin.yamlから自動的にメタデータを読み込みます
        super().__init__(app_context)
        self.stopwatch_window = None
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.after_id = None
        self.laps = []
    
    def initialize(self) -> bool:
        """初期化"""
        return True
    
    def create_widget(self, parent):
        """ウィジェットを作成"""
        frame = ctk.CTkFrame(parent)
        
        button = ctk.CTkButton(
            frame,
            text="⏲️ ストップウォッチを開く",
            command=self._open_stopwatch_window,
        )
        button.pack(pady=10, padx=20)
        
        return frame
    
    def _open_stopwatch_window(self):
        """ストップウォッチウィンドウを開く"""
        if self.stopwatch_window and self.stopwatch_window.winfo_exists():
            self.stopwatch_window.focus()
            return
        
        self.stopwatch_window = ctk.CTkToplevel()
        self.stopwatch_window.title("ストップウォッチ")
        self.stopwatch_window.geometry("350x500")
        
        # 時間表示
        self.time_label = ctk.CTkLabel(
            self.stopwatch_window,
            text="00:00:00.00",
            font=("Arial", 42, "bold"),
        )
        self.time_label.pack(pady=30)
        
        # コントロールボタン
        control_frame = ctk.CTkFrame(self.stopwatch_window)
        control_frame.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="開始",
            command=self._start_stopwatch,
            width=80,
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.lap_btn = ctk.CTkButton(
            control_frame,
            text="ラップ",
            command=self._record_lap,
            state="disabled",
            width=80,
        )
        self.lap_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(
            control_frame,
            text="リセット",
            command=self._reset_stopwatch,
            width=80,
        )
        self.reset_btn.pack(side="left", padx=5)
        
        # ラップタイム表示
        lap_label = ctk.CTkLabel(
            self.stopwatch_window,
            text="ラップタイム",
            font=("Arial", 14, "bold"),
        )
        lap_label.pack(pady=(20, 10))
        
        self.lap_frame = ctk.CTkScrollableFrame(
            self.stopwatch_window,
            height=200,
        )
        self.lap_frame.pack(pady=5, padx=20, fill="both", expand=True)
    
    def _start_stopwatch(self):
        """ストップウォッチを開始/停止"""
        if not self.is_running:
            # 開始
            self.is_running = True
            self.start_time = time.time() - self.elapsed_time
            self.start_btn.configure(text="停止")
            self.lap_btn.configure(state="normal")
            self._update_time()
        else:
            # 停止
            self.is_running = False
            self.start_btn.configure(text="開始")
            self.lap_btn.configure(state="disabled")
            if self.after_id:
                self.stopwatch_window.after_cancel(self.after_id)
    
    def _record_lap(self):
        """ラップタイムを記録"""
        if not self.is_running:
            return
        
        lap_time = self.elapsed_time
        self.laps.append(lap_time)
        
        # ラップ表示を追加
        lap_num = len(self.laps)
        minutes = int(lap_time // 60)
        seconds = int(lap_time % 60)
        centiseconds = int((lap_time % 1) * 100)
        
        lap_text = f"Lap {lap_num}: {minutes:02d}:{seconds:02d}.{centiseconds:02d}"
        lap_label = ctk.CTkLabel(
            self.lap_frame,
            text=lap_text,
            font=("Arial", 12),
        )
        lap_label.pack(anchor="w", pady=2)
    
    def _reset_stopwatch(self):
        """ストップウォッチをリセット"""
        if self.is_running:
            self._start_stopwatch()  # 停止
        
        self.elapsed_time = 0
        self.laps = []
        self._update_display()
        
        # ラップ表示をクリア
        for widget in self.lap_frame.winfo_children():
            widget.destroy()
    
    def _update_time(self):
        """時間を更新"""
        if not self.is_running:
            return
        
        self.elapsed_time = time.time() - self.start_time
        self._update_display()
        self.after_id = self.stopwatch_window.after(10, self._update_time)
    
    def _update_display(self):
        """表示を更新"""
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        centiseconds = int((self.elapsed_time % 1) * 100)
        
        self.time_label.configure(
            text=f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
        )
    
    def shutdown(self):
        """終了処理"""
        if self.is_running:
            self._start_stopwatch()  # 停止
        if self.stopwatch_window and self.stopwatch_window.winfo_exists():
            self.stopwatch_window.destroy()


# プラグインクラスをエクスポート
Plugin = StopwatchPlugin
```

## インストール方法

これらのプラグインをモノレポとして公開した場合、ユーザーは以下の方法でインストールできます：

### GUIから
1. プラグイン管理 → カタログから選択
2. `Nyayuta1060/horloq-official-plugins` を入力
3. 一覧から必要なプラグインを選択してインストール

### CLIから
```bash
# 個別にインストール
python -m horloq plugin install Nyayuta1060/horloq-official-plugins:hello
python -m horloq plugin install Nyayuta1060/horloq-official-plugins:timer
python -m horloq plugin install Nyayuta1060/horloq-official-plugins:stopwatch
```

## カスタマイズ

これらのサンプルプラグインをベースに、独自のプラグインを作成できます。
詳細は [プラグイン開発ガイド](PLUGIN_DEVELOPMENT.md) を参照してください。
