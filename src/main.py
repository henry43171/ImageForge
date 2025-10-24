# src/main.py
import json
from src.core.file_loader import FileLoader
from src.core.image_tools import ImageTools
from src.core.converter import ImageConverter 


def load_config(path="config/config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # === 初始化 ===
    loader = FileLoader()
    tools = ImageTools()
    converter = ImageConverter()

    # === 讀取參數 ===
    config = load_config()
    input_folder = config.get("input_img_folder", "input_img")
    output_folder = config.get("output_img_folder", "output_img")
    mode_status = config.get("mode_status", ["grey"])[2]

    # === 讀取圖片 ===
    paths = loader.list_image_files(input_folder)
    print(f"[INFO] 找到 {len(paths)} 張圖片")

    # === 模式分支 ===
    if mode_status == "grey":
        print("[INFO] 開始灰階量化...")
        tools.quantize_images(paths, output_folder, levels=4)

    elif mode_status == "compress":
        print("[INFO] 開始壓縮圖片...")
        tools.compress_images_in_folder(input_folder, output_folder, strength=5)

    elif mode_status == "rename":
        print("[INFO] 開始批量改名...")
        tools.batch_rename(input_folder, output_folder, prefix="new_name_", pad_digits = 6)

    elif mode_status == "icon":
        print("[INFO] 開始轉換成 icon...")
        converter.convert_images_to_icon(input_folder, output_folder, icon_sizes=[(32,32)])

    elif mode_status == "convert":
        print("[INFO] 開始格式轉換...")
        converter.convert_images_in_folder(input_folder, output_folder, "JPG")

    else:
        print(f"[ERROR] 未知模式：{mode_status}")

    print("[INFO] 處理結束！")


if __name__ == "__main__":
    main()
