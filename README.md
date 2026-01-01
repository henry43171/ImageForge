# ImageForge

ImageForge 是一個支援多功能圖片處理的整合工具，提供五種主要功能：多段灰階、影像壓縮、批量改名、icon 轉換以及圖片格式轉換。透過簡單直覺的 GUI 介面，用戶可以快速處理大量圖片而不需撰寫程式碼。

## 功能介紹
1. 多段灰階 (Grey)
   將圖片轉換為多段灰階，支援自訂灰階層數 (levels)，預設為 4 層。
2. 影像壓縮 (Compress)
   對整個資料夾的圖片進行壓縮，使用者可設定壓縮強度 (strength)，範圍 1–10。
3. 批量改名 (Rename)
   將資料夾內的圖片依指定前綴詞 (prefix) 重新命名，可設定數字補零位數 (pad_digits)。
4. Icon 轉換 (Icon)
   將圖片轉換為指定尺寸的 icon，可一次設定多個尺寸 (ex: (32,32))。
5. 圖片格式轉換 (Convert)
   將資料夾內圖片轉換為指定格式，如 JPG、PNG 或 WEBP。

## 安裝與執行
1. 安裝必要套件：
~~~bash
pip install customtkinter
~~~

2. 執行主程式：
~~~bash
python -m src.main_gui
~~~

3. 或使用 PyInstaller 打包成單一可執行檔：

點擊 `build.bat` 執行檔即可

## 使用方式
1. 選擇要執行的模式 (grey / compress / rename / icon / convert)。
2. 選擇輸入與輸出資料夾。
3. 根據模式設定對應的參數。
4. 點擊「🚀 執行任務」開始處理，Log 視窗會顯示處理進度與訊息。

## 系統需求
- Windows 10/11
- Python 3.10 以上
- 套件：customtkinter
- 輸入圖片格式：JPG, PNG, WEBP（視功能而定）

## 注意事項
- 確保輸入資料夾存在且包含有效圖片。
- 輸出資料夾會自動生成或覆寫同名檔案，請小心操作。
- main.py只是無GUI版本的接口，不影響整體執行。

