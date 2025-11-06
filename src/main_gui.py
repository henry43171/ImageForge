import customtkinter as ctk
import threading
import os
from tkinter import filedialog, messagebox
from src.core.file_loader import FileLoader
from src.core.image_tools import ImageTools
from src.core.converter import ImageConverter


class ImageProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # === 主題設定 ===
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("🧩 Image Processor GUI")
        self.geometry("760x580")
        self.resizable(False, False)

        # === 模組初始化 ===
        self.loader = FileLoader()
        self.tools = ImageTools()
        self.converter = ImageConverter()

        # === 狀態變數 ===
        self.input_folder = ctk.StringVar(value="input_img")
        self.output_folder = ctk.StringVar(value="output_img")
        self.mode = ctk.StringVar(value="grey")

        # 參數表 (依模式顯示)
        self.param_entries = {}

        # === 介面建立 ===
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="🧩 Image Processing Tool", font=("Segoe UI", 20, "bold")).pack(pady=10)

        # 模式選單
        frame_mode = ctk.CTkFrame(self)
        frame_mode.pack(pady=5, fill="x", padx=20)
        ctk.CTkLabel(frame_mode, text="模式：", width=80, anchor="e").pack(side="left", padx=10)
        mode_menu = ctk.CTkOptionMenu(
            frame_mode,
            variable=self.mode,
            values=["grey", "compress", "rename", "icon", "convert"],
            command=self.on_mode_change
        )
        mode_menu.pack(side="left", padx=10)

        # 輸入/輸出資料夾
        self.make_folder_selector("輸入資料夾：", self.input_folder)
        self.make_folder_selector("輸出資料夾：", self.output_folder)

        # 動態參數框架
        self.param_frame = ctk.CTkFrame(self)
        self.param_frame.pack(pady=10, fill="x", padx=20)
        ctk.CTkLabel(self.param_frame, text="參數設定", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=5)
        self.param_container = ctk.CTkFrame(self.param_frame)
        self.param_container.pack(fill="x", padx=10)
        self.populate_params("grey")  # 預設參數

        # 執行按鈕
        self.run_button = ctk.CTkButton(self, text="🚀 執行任務", command=self.run_task)
        self.run_button.pack(pady=15)

        # Log 視窗
        self.log_box = ctk.CTkTextbox(self, width=700, height=200)
        self.log_box.pack(padx=20, pady=10)
        self.log("[INFO] 系統初始化完成。")

    # -----------------------
    # 📂 資料夾選擇
    # -----------------------
    def make_folder_selector(self, label_text, var):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=3, fill="x", padx=20)
        ctk.CTkLabel(frame, text=label_text, width=100, anchor="e").pack(side="left", padx=10)
        ctk.CTkEntry(frame, textvariable=var, width=420).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="選擇", width=80,
                      command=lambda: var.set(filedialog.askdirectory() or var.get())).pack(side="left", padx=5)

    # -----------------------
    # 🔧 動態參數區域
    # -----------------------
    def populate_params(self, mode):
        """依模式更新參數輸入欄位"""
        for widget in self.param_container.winfo_children():
            widget.destroy()
        self.param_entries.clear()

        params_by_mode = {
            "grey": {"levels": 4},
            "compress": {"strength": 5},
            "rename": {"prefix": "new_name_", "pad_digits": 6},
            "icon": {"icon_sizes": "(32,32)"},
            "convert": {"format": "JPG"},
        }

        params = params_by_mode.get(mode, {})

        if not params:
            ctk.CTkLabel(self.param_container, text="此模式無需參數設定").pack(pady=5)
            return

        for i, (key, default) in enumerate(params.items()):
            frame = ctk.CTkFrame(self.param_container)
            frame.pack(fill="x", pady=3)
            ctk.CTkLabel(frame, text=f"{key}：", width=120, anchor="e").pack(side="left", padx=5)
            entry = ctk.CTkEntry(frame, width=200)
            entry.insert(0, str(default))
            entry.pack(side="left", padx=5)
            self.param_entries[key] = entry

    def on_mode_change(self, mode):
        self.populate_params(mode)

    # -----------------------
    # 🪵 Log 輸出
    # -----------------------
    def log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.update_idletasks()

    # -----------------------
    # 🚀 執行邏輯
    # -----------------------
    def run_task(self):
        self.run_button.configure(state="disabled", text="執行中...")
        thread = threading.Thread(target=self._run_main)
        thread.start()

    def _run_main(self):
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()
        mode = self.mode.get()
        params = {k: v.get() for k, v in self.param_entries.items()}

        if not os.path.exists(input_folder):
            messagebox.showerror("錯誤", f"找不到輸入資料夾：{input_folder}")
            self.run_button.configure(state="normal", text="🚀 執行任務")
            return

        try:
            self.log(f"[INFO] 模式：{mode}")
            self.log(f"[INFO] 參數：{params}")

            paths = self.loader.list_image_files(input_folder)
            self.log(f"[INFO] 找到 {len(paths)} 張圖片")

            if mode == "grey":
                levels = int(params.get("levels", 4))
                self.tools.quantize_images(paths, output_folder, levels=levels)
            elif mode == "compress":
                strength = int(params.get("strength", 5))
                self.tools.compress_images_in_folder(input_folder, output_folder, strength=strength)
            elif mode == "rename":
                prefix = params.get("prefix", "new_name_")
                pad_digits = int(params.get("pad_digits", 6))
                self.tools.batch_rename(input_folder, output_folder, prefix=prefix, pad_digits=pad_digits)
            elif mode == "icon":
                sizes_str = params.get("icon_sizes", "(32,32)")
                icon_sizes = [eval(sizes_str)] if sizes_str else [(32, 32)]
                self.converter.convert_images_to_icon(input_folder, output_folder, icon_sizes=icon_sizes)
            elif mode == "convert":
                fmt = params.get("format", "JPG")
                self.converter.convert_images_in_folder(input_folder, output_folder, fmt)
            else:
                self.log(f"[ERROR] 未知模式：{mode}")
                return

            self.log("[INFO] ✅ 處理完成。")

        except Exception as e:
            self.log(f"[ERROR] {e}")

        finally:
            self.run_button.configure(state="normal", text="🚀 執行任務")


if __name__ == "__main__":
    app = ImageProcessorApp()
    app.mainloop()
