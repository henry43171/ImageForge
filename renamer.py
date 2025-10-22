# renamer.py
import os
from PIL import Image
from typing import List, Tuple

def batch_rename(input_folder: str, prefix: str = "", start_index: int = 1, pad_digits: int = 5) -> List[Tuple[str, Image.Image]]:
    """
    批量改名資料夾內的圖片，檔案格式不變
    - prefix: 檔名前綴
    - start_index: 流水號起始值
    - pad_digits: 流水號位數，例如 4 -> 0001, 0002 ...
    
    Returns:
        List[Tuple[新檔名完整路徑, Image.Image]]
    """
    results = []
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    files.sort()  # 保持順序一致

    index = start_index
    for fname in files:
        old_path = os.path.join(input_folder, fname)
        name, ext = os.path.splitext(fname)
        new_name = f"{prefix}{str(index).zfill(pad_digits)}{ext}"
        new_path = os.path.join(input_folder, new_name)

        try:
            os.rename(old_path, new_path)
            with Image.open(new_path) as img:
                results.append((new_path, img.copy()))
            index += 1
        except Exception as e:
            print(f"[ERROR] 無法改名 {fname}: {e}")

    return results
