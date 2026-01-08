@echo off
REM Windowsローカルビルドスクリプト

echo Building Horloq...

REM PyInstallerがインストールされているか確認
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM ビルド
echo Creating binary...
pyinstaller build.spec

REM 結果を表示
echo.
echo Build complete!
echo Binary file: dist\horloq.exe
echo.
echo To run:
echo   dist\horloq.exe
pause
