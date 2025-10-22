# load_img.py
import os
from typing import List, Tuple
from PIL import Image


# 取得檔案清單
def list_image_files(input_folder: str, exts: List[str] = None) -> List[str]:
    """
    回傳資料夾內所有檔案的完整路徑（可選副檔名過濾）
    - exts: 可接受的副檔名列表，例如 ['.png', '.jpg']（小寫）
    """
    if exts is None:
        exts = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"]

    files = []
    for fname in os.listdir(input_folder):
        full = os.path.join(input_folder, fname)
        if not os.path.isfile(full):
            continue
        _, ext = os.path.splitext(fname)
        if ext.lower() in exts:
            files.append(full)
    return files


# 儲存處理後的影像
def save_images(images: List[Tuple[str, Image.Image]], input_folder: str, output_folder: str):
    """
    將 [(path, image), ...] 儲存到 output_folder。
    會保留原始檔名。
    """
    os.makedirs(output_folder, exist_ok=True)

    for path, img in images:
        fname = os.path.basename(path)
        output_path = os.path.join(output_folder, fname)

        try:
            img.save(output_path)
            print(f"[INFO] 已儲存：{output_path}")
        except Exception as e:
            print(f"[ERROR] 無法儲存 {output_path}: {e}")

