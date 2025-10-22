# main.py
import load_img
import grey_quantize

def main():
    # 設定參數
    input_folder = "input_img"
    output_folder = "output_img"

    # 讀取圖片
    paths = load_img.list_image_files(input_folder)
    print(f"找到 {len(paths)} 張圖片")
    print(f"開始圖片轉換")

    # 功能(轉灰階)
    quantized_images = grey_quantize.quantize_images(paths, levels=2)

    # 存檔
    load_img.save_images(quantized_images, input_folder, output_folder)
    print(f"圖片轉換結束")


if __name__ == "__main__":
    main()
