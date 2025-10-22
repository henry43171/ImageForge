# grey_quantize.py
import os
from typing import List, Tuple
from PIL import Image


# 路徑清單轉成灰階影像物件
def quantize_gray(value: int, levels: int) -> int:
    """將單個灰階像素量化到指定層數"""
    if levels <= 1:
        return 0
    elif levels == 2:
        return 0 if value < 128 else 255
    else:
        factor = 256 // levels
        return int(value / 256 * levels) * factor


def quantize_images(paths: List[str], levels: int = 5) -> List[Tuple[str, Image.Image]]:
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
                img_quant = img_gray.point(lambda x: quantize_gray(x, levels))
                results.append((p, img_quant.copy()))
        except Exception as e:
            print(f"[ERROR] 無法處理 {p}: {e}")
    return results
