# compress.py
import os
from PIL import Image
from typing import List, Tuple


def compress_images_in_folder(input_folder: str, strength: int = 5) -> List[Tuple[str, Image.Image]]:
    """
    批量壓縮資料夾中的圖片，回傳壓縮後的影像物件清單。
    支援格式：JPEG, JPG, WEBP, PNG
    - strength: 1~10，數字越大壓縮越多

    Args:
        input_folder (str): 原圖資料夾
        strength (int): 壓縮強度，1~10

    Returns:
        List[Tuple[str, Image.Image]]: [(檔名, 壓縮後的影像)]
    """
    strength = max(1, min(10, strength))
    results: List[Tuple[str, Image.Image]] = []

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        if not os.path.isfile(input_path):
            continue

        ext = os.path.splitext(filename)[1].lower()
        if ext not in [".jpg", ".jpeg", ".webp", ".png"]:
            print(f"[SKIP] {filename} 不支援的格式")
            continue

        try:
            with Image.open(input_path) as img:
                img = img.convert("RGB")  # 保險起見轉成RGB，避免透明圖報錯

                # 模擬壓縮效果：根據strength做不同品質的副本
                if ext in [".jpg", ".jpeg", ".webp"]:
                    quality = max(1, 95 - (strength * 9))
                    # Pillow 無法直接在記憶體壓縮 -> 透過 BytesIO 模擬壓縮
                    from io import BytesIO
                    buffer = BytesIO()
                    img.save(buffer, format="JPEG", quality=quality)
                    buffer.seek(0)
                    compressed = Image.open(buffer).copy()
                    buffer.close()

                elif ext == ".png":
                    compress_level = min(strength, 9)
                    from io import BytesIO
                    buffer = BytesIO()
                    img.save(buffer, format="PNG", compress_level=compress_level)
                    buffer.seek(0)
                    compressed = Image.open(buffer).copy()
                    buffer.close()

                results.append((filename, compressed))
                print(f"[INFO] {filename} 壓縮完成")

        except Exception as e:
            print(f"[ERROR] 無法壓縮 {filename}: {e}")

    return results
