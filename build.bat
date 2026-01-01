@echo off

REM 切到此 bat 所在資料夾（專案根目錄）
cd /d %~dp0

echo === Build EXE with PyInstaller ===

pyinstaller ^
  --onefile ^
  --windowed ^
  --name ImageForgeGUI ^
  --paths . ^
  --add-data "config\config.json;config" ^
  src\main_gui.py

echo.
echo === Cleaning temporary files ===

REM 刪除 build 資料夾
if exist build (
    rmdir /s /q build
    echo Removed build folder
)

REM 刪除 spec 檔
if exist ImageForgeGUI.spec (
    del /f /q ImageForgeGUI.spec
    echo Removed spec file
)

echo.
echo === Done ===
pause
