import os
from typing import List, Tuple
from PIL import Image

# -------------------------
# 1) 只負責取得檔案清單（路徑）
# -------------------------
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


# -------------------------
# 2) 只負責把路徑清單轉成灰階影像物件（不存檔）
# -------------------------
def load_paths_to_grayscale(paths: List[str]) -> List[Tuple[str, Image.Image]]:
    """
    接收 image path 的 list，回傳 [(path, gray_image), ...]
    - 這裡會把 Image 物件複製一份再回傳，避免 with 關閉造成的問題
    """
    results = []
    for p in paths:
        try:
            with Image.open(p) as img:
                gray = img.convert("L")
                results.append((p, gray.copy()))
        except Exception as e:
            print(f"[ERROR] 無法讀取或轉換 {p}: {e}")
    return results


# -------------------------
# 3) 只負責儲存處理後的影像
# -------------------------
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
    print(f"全圖片路徑:\n {paths}")

    # 功能(轉灰階)
    gray_images = load_paths_to_grayscale(paths)
    for path, img in gray_images:
        print(f"已載入灰階：{path} (size={img.size})")
    print(f"gray_images:\n {gray_images}")
    
    # 存檔
    save_images(gray_images, input_folder, output_folder)
