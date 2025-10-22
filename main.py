# main.py
import load_img
import grey_quantize
import compress
import convert_icon
import convert

def main():
    # 設定參數
    input_folder = "input_img"
    output_folder = "output_img"
    mode_status = "convert"

    # 讀取圖片
    paths = load_img.list_image_files(input_folder)
    print(f"找到 {len(paths)} 張圖片")
    print(f"開始圖片轉換")

    # 功能
    if mode_status == "grey": 
        # 轉灰階
        quantized_images = grey_quantize.quantize_images(paths, levels=2)
        # 存檔
        load_img.save_images(quantized_images, input_folder, output_folder)
        print(f"圖片轉換結束")

    elif mode_status == "compress":
        # 壓縮
        quantized_images = compress.compress_images_in_folder(input_folder, strength=4)
        # 存檔
        load_img.save_images(quantized_images, input_folder, output_folder)
        print(f"圖片轉換結束")
    
    elif mode_status == "icon":
        # 轉icon
        quantized_images = convert_icon.convert_images_to_icon(input_folder, output_folder, icon_sizes=[(32, 32)])
    
    elif mode_status == "convert":
        # 轉檔
        quantized_images = convert.convert_images_in_folder(input_folder, output_folder, "JPEG")



if __name__ == "__main__":
    main()
