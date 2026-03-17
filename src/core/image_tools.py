# src/core/img_tool.py
import os
from PIL import Image
from typing import List, Tuple

class ImageTools:
    
    def compress_images_in_folder(self, input_folder: str, output_folder: str, strength: int = 5):
        """
        即時壓縮資料夾中的圖片，並直接儲存到 output_folder。
        支援格式：JPEG, JPG, WEBP, PNG
        - strength: 1~10，數字越大壓縮越多
        """
        strength = max(1, min(10, strength))
        os.makedirs(output_folder, exist_ok=True)

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

                    # 模擬壓縮效果
                    from io import BytesIO
                    if ext in [".jpg", ".jpeg", ".webp"]:
                        quality = max(1, 95 - (strength * 9))
                        buffer = BytesIO()
                        img.save(buffer, format="JPEG", quality=quality)
                        buffer.seek(0)
                        compressed = Image.open(buffer)
                        save_path = os.path.join(output_folder, filename)
                        compressed.save(save_path, format="JPEG", quality=quality)
                        buffer.close()

                    elif ext == ".png":
                        compress_level = min(strength, 9)
                        buffer = BytesIO()
                        img.save(buffer, format="PNG", compress_level=compress_level)
                        buffer.seek(0)
                        compressed = Image.open(buffer)
                        save_path = os.path.join(output_folder, filename)
                        compressed.save(save_path, format="PNG", compress_level=compress_level)
                        buffer.close()

                    print(f"[INFO] {filename} 壓縮完成並儲存到：{save_path}")

            except Exception as e:
                print(f"[ERROR] 無法壓縮 {filename}: {e}")


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


    def quantize_images(self, paths: List[str], output_folder: str = "output_img", levels: int = 5):
        """
        即時處理 + 即時儲存灰階量化圖片
        - 不回傳結果
        """
        os.makedirs(output_folder, exist_ok=True)

        for p in paths:
            try:
                with Image.open(p) as img:
                    # 🔥 關鍵：轉 HSV，取 V (亮度)
                    img_hsv = img.convert("HSV")
                    h, s, v = img_hsv.split()

                    # 用 V 當作灰階（已經去除固有色）
                    img_gray = v

                    # 灰階量化
                    img_quant = img_gray.point(lambda x: self.quantize_gray(x, levels))

                    # 儲存
                    fname = os.path.basename(p)
                    save_path = os.path.join(output_folder, fname)
                    img_quant.save(save_path)

                    print(f"[INFO] 已完成並儲存：{save_path}")

            except Exception as e:
                print(f"[ERROR] 無法處理 {p}: {e}")


    def batch_rename(
        self, 
        input_folder: str, 
        output_folder: str = "renamed_img",
        prefix: str = "", 
        start_index: int = 1, 
        pad_digits: int = 5
        ):
        """
        批量重新命名圖片（即時儲存版本）
        - prefix: 新檔名前綴
        - start_index: 流水號起始值
        - pad_digits: 流水號位數，例如 4 -> 0001, 0002 ...
        - output_folder: 輸出資料夾，不覆蓋原檔
        """
        os.makedirs(output_folder, exist_ok=True)

        files = [
            f for f in os.listdir(input_folder)
            if os.path.isfile(os.path.join(input_folder, f))
        ]
        files.sort()  # 保持一致的順序

        index = start_index
        for fname in files:
            old_path = os.path.join(input_folder, fname)
            _, ext = os.path.splitext(fname)
            new_name = f"{prefix}{str(index).zfill(pad_digits)}{ext}"
            new_path = os.path.join(output_folder, new_name)

            try:
                with Image.open(old_path) as img:
                    img.save(new_path)
                    print(f"[INFO] {fname} → {new_name}")
                index += 1

            except Exception as e:
                print(f"[ERROR] 無法處理 {fname}: {e}")