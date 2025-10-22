# convert_icon.py
import os
from PIL import Image
from typing import List, Tuple

def convert_images_to_icon(input_folder, output_folder, icon_sizes=[(32,32)]):
    """
    將資料夾內所有圖片轉成 ICO
    - icon_sizes: list of tuples，指定 ICO 尺寸，例如 [(16,16), (32,32), (48,48)]
    """
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        if not os.path.isfile(input_path):
            continue

        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}.ico")

        try:
            with Image.open(input_path) as img:
                img.save(output_path, format="ICO", sizes=icon_sizes)
                print(f"[INFO] {filename} -> {output_path} 成功！")
        except Exception as e:
            print(f"[ERROR] 無法轉換 {filename} 為 ICO: {e}")

