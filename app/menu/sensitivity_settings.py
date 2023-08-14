import win32gui
import win32con
import tkinter as tk
from posture_analyser import PostureAnalyser
from shared_config import SharedConfig
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import threading


class SensitivitySettings:
    def __init__(self, shared_config: SharedConfig, start_new_worker):
        self.config: SharedConfig = shared_config
        self.analyzer = PostureAnalyser(shared_config)
        self.stop = False
        self.root = None
        self.start_new_worker = start_new_worker
        self.chances_sitting_wrong = 0

    def update_frame_label(self, user_image, root):
        frame_image = self.get_frame_image()
        user_image.config(image=frame_image)
        user_image.image = frame_image
        root.update()
        if not self.stop:
            root.after(30, self.update_frame_label, user_image, root)

    def get_frame_image(self):
        invalid, frame, chances_sitting_wrong = self.analyzer.calculate_if_show_overlay(
            False)
        self.chances_sitting_wrong = chances_sitting_wrong
        if frame is None:
            empty_image = Image.new("RGBA", (160, 90), (0, 0, 0, 0))
            return ImageTk.PhotoImage(empty_image)
        modified_img = np.where(frame < 1, 0, 255)
        pil_image = Image.fromarray(modified_img.astype(np.uint8))

        if invalid:
            border_color = "red"
        else:
            border_color = "green"

        pil_image = Image.fromarray(modified_img)
        bordered_image = Image.new(
            "RGB", (pil_image.width + 10, pil_image.height + 10), border_color)
        bordered_image.paste(pil_image, (5, 5))

        frame_image = ImageTk.PhotoImage(bordered_image)
        return frame_image

    def on_closing(self):
        self.analyzer.calculate_if_show_overlay(True)  # release camera
        self.stop = True
        self.root.destroy()
        self.root = None
        self.start_new_worker()

    def on_sensitivity_slider_change(self, value):
        self.config.certainty = int(value)/100
        self.config.save_to_file()

    def create_window(self):
        self.root = root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        hwnd = int(root.winfo_id())
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
            hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST)
        win32gui.SetLayeredWindowAttributes(
            hwnd, 0, int(255 * 0.5), win32con.LWA_ALPHA)
        root.lift()
        root.focus_force()
        root.grab_set()
        root.grab_release()
        root.attributes("-topmost", True)

        frame_img = self.get_frame_image()
        user_image = tk.Label(root, image=frame_img)
        user_image.image = frame_img

        root.geometry("500x300")

        self.update_frame_label(user_image, root)

        user_image.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        slider = tk.Scale(root, from_=1, to=99, orient="horizontal",
                          length=300, command=self.on_sensitivity_slider_change)
        slider.set(self.config.certainty*100)

        slider.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        strict_label = tk.Label(root, text="Strict")
        loose_label = tk.Label(root, text="Loose")
        strict_label.place(relx=0.1, rely=0.5, anchor=tk.CENTER)
        loose_label.place(relx=0.9, rely=0.5, anchor=tk.CENTER)

        auto_adjust_label = tk.Label(
            root, text="Please ensure you're sitting in the best posture you can. Adjust your chair and body position to sit comfortably and correctly. When you are ready click auto adjust to adjust the strictness of the application to your current posture",
            wraplength=450)
        auto_adjust_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        def set_slider(): return slider.set(min(self.chances_sitting_wrong+10, 99))
        btn_auto_adjust = tk.Button(
            root, text="Auto adjust", command=set_slider)

        btn_auto_adjust.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        start_button = tk.Button(
            root, text="Start", command=self.on_closing, fg="green")

        start_button.place(relx=0.8, rely=0.9, anchor=tk.CENTER)

        root.after(300, self.update_frame_label, user_image, root)
        root.mainloop()

    def show(self):
        self.stop = False
        window_thread = threading.Thread(
            target=self.create_window)
        window_thread.daemon = True
        window_thread.start()
