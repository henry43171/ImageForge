# convert.py
import os
from PIL import Image
from pillow_heif import register_heif_opener
from typing import List, Tuple

# 註冊 HEIC 支援
register_heif_opener()

# 支援輸出格式
format_map = {
    "JPG": "JPEG",
    "JPEG": "JPEG",
    "PNG": "PNG",
    "WEBP": "WEBP"
}

def convert_images_in_folder(input_folder, output_folder, output_format):
    """
    將資料夾內所有圖片轉換成指定格式
    - 支援 PNG/JPEG/WEBP/HEIC 輸入與輸出
    - 保留原檔名，只改副檔名
    - 遇到不支援格式或錯誤會自動跳過
    """
    output_format_upper = format_map.get(output_format.upper())
    if not output_format_upper:
        print(f"[ERROR] 不支援的輸出格式: {output_format}")
        return

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        if not os.path.isfile(input_path):
            continue

        name, _ = os.path.splitext(filename)
        # 生成輸出檔名副檔名
        output_ext = output_format_upper.lower() if output_format_upper != "JPEG" else "jpg"
        output_path = os.path.join(output_folder, f"{name}.{output_ext}")

        try:
            with Image.open(input_path) as img:
                # JPEG 輸出需轉 RGB
                if output_format_upper == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(output_path, format=output_format_upper)
                print(f"[INFO] {filename} -> {output_path} 成功！")
        except Exception as e:
            print(f"[ERROR] 無法轉換 {filename}: {e}")

