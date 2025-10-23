# src/main.py
from src.core.file_loader import FileLoader
from src.core.image_tools import ImageTools
from src.core.converter import ImageConverter 

def main():
    # === 初始化 ===
    loader = FileLoader()
    tools = ImageTools()
    converter = ImageConverter()  # 若有轉檔相關功能時啟用

    # === 參數設定 ===
    input_folder = "input_img"
    output_folder = "output_img"
    mode_status = "rename"  # grey / compress / rename / icon / convert

    # === 讀取圖片 ===
    paths = loader.list_image_files(input_folder)
    print(f"[INFO] 找到 {len(paths)} 張圖片")

    # === 模式分支 ===
    if mode_status == "grey":
        print("[INFO] 開始灰階量化...")
        results = tools.quantize_images(paths, levels=4)
        print(results)
        loader.save_images(results, input_folder, output_folder)

    elif mode_status == "compress":
        print("[INFO] 開始壓縮圖片...")
        results = tools.compress_images_in_folder(input_folder, strength=5)
        loader.save_images(results, input_folder, output_folder)

    elif mode_status == "rename":
        print("[INFO] 開始批量改名...")
        results = tools.batch_rename(input_folder, prefix="new_name_", pad_digits = 6)
        loader.save_images(results, input_folder, output_folder)

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
