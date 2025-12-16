"""
Horloq - 拡張可能デスクトップ据え置き時計

エントリーポイント
"""

import sys
from pathlib import Path
from horloq.core.app import HorloqApp


def main():
    """メイン関数"""
    # コマンドライン引数の処理
    config_path = None
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    
    # アプリケーションを作成して起動
    app = HorloqApp(config_path)
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nアプリケーションを終了します...")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
