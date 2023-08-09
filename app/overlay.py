import win32gui
import win32con
import tkinter as tk
from shared_config import SharedConfig
import tkinter as tk
from PIL import Image, ImageTk
from screeninfo import get_monitors
import os
from db.db import get_statistics_by_num_days
import numpy as np


class Overlay:
    def __init__(self, shared_config: SharedConfig):
        self.config = shared_config
        self.overlay: tk.Tk = None
        self.frame = None

    def create_overlay(self, disable_for_15_min, disable_for_today, updateStatus):
        monitors = get_monitors()
        overlay = tk.Tk()
        monitor = monitors[self.config.monitor]
        overlay.geometry(
            f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")

        overlay.attributes('-alpha', 0.8)  # overlay transparency
        hwnd = int(overlay.winfo_id())
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
            hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST)
        win32gui.SetLayeredWindowAttributes(
            hwnd, 0, int(255 * 0.5), win32con.LWA_ALPHA)
        overlay.lift()
        overlay.focus_force()
        overlay.grab_set()
        overlay.grab_release()
        overlay.attributes("-topmost", True)

        image1 = Image.open(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "assets", "images", "bonk.png"))
        bonk_image = ImageTk.PhotoImage(image1)

        frame_image_label = tk.Label(image=bonk_image)
        frame_image_label.image = bonk_image

        frame_img = self.get_frame_image()
        __frame_label = tk.Label(image=frame_img)
        __frame_label.image = frame_img
        self.update_frame_label(__frame_label, overlay)

        statistics = get_statistics_by_num_days(1)
        if len(statistics) > 0:
            (total_valid_time, total_invalid_time, date) = statistics[0]
            label = tk.Label(overlay, text="Today you were sitting correctly for: "+str(int(
                total_valid_time))+" minutes", font=("Arial", 24), bg="white", fg="black", compound="top")
            label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        frame_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        __frame_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        label = tk.Label(overlay, text=self.config.alarm_message, font=(
            "Arial", 24), bg="white", fg="black", compound="top")
        label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        btn_15_min = tk.Button(overlay, text="Disable for 15 min", command=disable_for_15_min, font=(
            "Arial", 24),  fg="green", bg="black")
        btn_15_min.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        btn_today = tk.Button(overlay, text="Disable for today", command=disable_for_today, font=(
            "Arial", 24),  fg="green", bg="black")
        btn_today.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        overlay.after(300, updateStatus)

        return overlay

    def update_frame_label(self, __frame_label, overlay):
        frame_image = self.get_frame_image()
        __frame_label.config(image=frame_image)
        __frame_label.image = frame_image
        overlay.after(100, self.update_frame_label, __frame_label, overlay)

    def get_frame_image(self):
        modified_img = np.where(self.frame < 1, 0, 255)

        pil_image = Image.fromarray(modified_img.astype(np.uint8))

        frame_image = ImageTk.PhotoImage(pil_image)
        return frame_image
