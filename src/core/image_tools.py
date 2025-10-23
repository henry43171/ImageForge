# src/core/img_tool.py
import os
from PIL import Image
from typing import List, Tuple

class ImageTools:
    
    def compress_images_in_folder(self, input_folder: str, strength: int = 5) -> List[Tuple[str, Image.Image]]:
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


    # 路徑清單轉成灰階影像物件
    def quantize_gray(self, value: int, levels: int) -> int:
        """將單個灰階像素量化到指定層數"""
        if levels <= 1:
            return 0
        elif levels == 2:
            return 0 if value < 128 else 255
        else:
            factor = 256 // levels
            return int(value / 256 * levels) * factor


    def quantize_images(self, paths: List[str], levels: int = 5) -> List[Tuple[str, Image.Image]]:
        """
        接收圖片路徑清單，進行灰階量化（不存檔）
        - 回傳格式: [(path, quantized_image), ...]
        """
        results = []
        for p in paths:
            try:
                with Image.open(p) as img:
                    # 轉灰階
                    img_gray = img.convert("L")
                    # 灰階量化
                    img_quant = img_gray.point(lambda x: self.quantize_gray(x, levels))
                    results.append((p, img_quant.copy()))
            except Exception as e:
                print(f"[ERROR] 無法處理 {p}: {e}")
        return results


    def batch_rename(self, input_folder: str, prefix: str = "", start_index: int = 1, pad_digits: int = 5) -> List[Tuple[str, Image.Image]]:
        """
        批量產生改名前綴 + 流水號的圖片清單，但不改動原始檔案
        - prefix: 檔名前綴
        - start_index: 流水號起始值
        - pad_digits: 流水號位數，例如 4 -> 0001, 0002 ...
        
        Returns:
            List[Tuple[模擬新檔名完整路徑, Image.Image]]
        """
        results = []
        files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
        files.sort()  # 保持順序一致

        index = start_index
        for fname in files:
            old_path = os.path.join(input_folder, fname)
            _, ext = os.path.splitext(fname)
            # 只生成新名稱，路徑暫存於 results，不影響原檔案
            new_name = f"{prefix}{str(index).zfill(pad_digits)}{ext}"
            new_path = os.path.join(input_folder, new_name)

            try:
                with Image.open(old_path) as img:
                    results.append((new_path, img.copy()))
                index += 1
            except Exception as e:
                print(f"[ERROR] 無法處理 {fname}: {e}")

        return results

