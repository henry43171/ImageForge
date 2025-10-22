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


# -------------------------
# 範例
# -------------------------
if __name__ == "__main__":
    # 設定參數
    input_folder = "input_img"
    output_folder = "output_img"

    # 讀取圖片
    paths = list_image_files(input_folder)
    print(f"找到 {len(paths)} 張圖片")
    print(f"開始圖片轉換")

    # 功能(轉灰階)
    quantized_images = quantize_images(paths, levels=2)

    # 存檔
    save_images(quantized_images, input_folder, output_folder)
    print(f"圖片轉換結束")
