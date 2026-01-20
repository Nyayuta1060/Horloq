#!/usr/bin/env python3
"""
アイコンファイル生成スクリプト
icon.pngから各プラットフォーム用のアイコンを生成します
"""

from PIL import Image
import os

def generate_ico(png_path: str, ico_path: str):
    """Windows用.icoファイルを生成"""
    img = Image.open(png_path)
    # 複数サイズを含むicoファイルを作成
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, format='ICO', sizes=sizes)
    print(f"[OK] {ico_path} を生成しました")

def generate_icns(png_path: str, icns_path: str):
    """macOS用.icnsファイルを生成"""
    try:
        import subprocess
        img = Image.open(png_path)
        
        # iconsetディレクトリを作成
        iconset_dir = "icon.iconset"
        os.makedirs(iconset_dir, exist_ok=True)
        
        # 各サイズのPNGを生成
        sizes = [16, 32, 128, 256, 512]
        for size in sizes:
            # 通常解像度
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(f"{iconset_dir}/icon_{size}x{size}.png")
            # Retina解像度（2x）
            resized_2x = img.resize((size * 2, size * 2), Image.Resampling.LANCZOS)
            resized_2x.save(f"{iconset_dir}/icon_{size}x{size}@2x.png")
        
        # iconutilコマンドでicnsに変換（macOSのみ）
        if os.path.exists("/usr/bin/iconutil"):
            result = subprocess.run(
                ["iconutil", "-c", "icns", iconset_dir, "-o", icns_path],
                capture_output=True
            )
            if result.returncode == 0:
                print(f"[OK] {icns_path} を生成しました")
            else:
                print(f"[WARN] iconutil実行エラー（macOS以外では正常）: {result.stderr.decode()}")
        else:
            print(f"[WARN] iconutilが見つかりません（macOS以外では正常）")
        
        # iconsetディレクトリをクリーンアップ
        import shutil
        shutil.rmtree(iconset_dir)
        
    except Exception as e:
        print(f"⚠ .icns生成中にエラー: {e}")
        print("  macOS以外の環境では.icnsは不要です")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    png_path = os.path.join(base_dir, "icon.png")
    
    if not os.path.exists(png_path):
        print(f"エラー: {png_path} が見つかりません")
        return
    
    # Windows用.icoを生成
    ico_path = os.path.join(base_dir, "icon.ico")
    generate_ico(png_path, ico_path)
    
    # macOS用.icnsを生成（macOS環境のみ）
    icns_path = os.path.join(base_dir, "icon.icns")
    generate_icns(png_path, icns_path)
    
    print("\n完了しました！")

if __name__ == "__main__":
    main()
