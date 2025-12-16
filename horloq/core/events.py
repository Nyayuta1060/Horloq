"""
イベントシステム
"""

from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    """イベントデータ"""
    name: str
    data: Any
    timestamp: datetime


class EventManager:
    """イベント管理システム"""
    
    def __init__(self):
        """初期化"""
        self._listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event_name: str, callback: Callable):
        """
        イベントリスナーを登録
        
        Args:
            event_name: イベント名
            callback: コールバック関数
        """
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        
        if callback not in self._listeners[event_name]:
            self._listeners[event_name].append(callback)
    
    def off(self, event_name: str, callback: Callable):
        """
        イベントリスナーを解除
        
        Args:
            event_name: イベント名
            callback: コールバック関数
        """
        if event_name in self._listeners:
            if callback in self._listeners[event_name]:
                self._listeners[event_name].remove(callback)
    
    def emit(self, event_name: str, data: Any = None):
        """
        イベントを発行
        
        Args:
            event_name: イベント名
            data: イベントデータ
        """
        if event_name not in self._listeners:
            return
        
        event = Event(name=event_name, data=data, timestamp=datetime.now())
        
        for callback in self._listeners[event_name]:
            try:
                callback(event)
            except Exception as e:
                print(f"イベント処理エラー ({event_name}): {e}")
    
    def clear(self, event_name: str = None):
        """
        イベントリスナーをクリア
        
        Args:
            event_name: イベント名（Noneの場合は全てクリア）
        """
        if event_name is None:
            self._listeners.clear()
        elif event_name in self._listeners:
            del self._listeners[event_name]
    
    def list_events(self) -> List[str]:
        """
        登録されているイベント名のリストを取得
        
        Returns:
            イベント名のリスト
        """
        return list(self._listeners.keys())
    
    def listener_count(self, event_name: str) -> int:
        """
        指定イベントのリスナー数を取得
        
        Args:
            event_name: イベント名
            
        Returns:
            リスナー数
        """
        return len(self._listeners.get(event_name, []))
