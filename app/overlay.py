import win32gui
import win32con
import tkinter as tk
import threading
import datetime
from shared_config import SharedConfig 
import tkinter as tk
from PIL import Image, ImageTk
from screeninfo import get_monitors
import time
import os 
from db.db import save_statistics_to_db, get_statistics_by_num_days

class ScreenOverlayRunner:
    def __init__(self, shared_config:SharedConfig, show_overlay_function):
        self.config = shared_config
        self.overlay:tk.Tk = None
        self.disabledTimer = 0
        self.show_overlay_function = show_overlay_function
        self.valid_time=0
        self.invalid_time=0
        self.timer = None
        self.invalid_position_consecutive_checks_seconds = 0

    def disable_for_15_min(self):
        self.disabledTimer= 15 * 60

    def disable_for_today(self):
        def time_till_midnight():
            now = datetime.datetime.now()
            midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
            midnight = midnight + datetime.timedelta(days=1)
            time_remaining = midnight - now
            return time_remaining.total_seconds()

        self.disabledTimer = time_till_midnight()

    def create_overlay(self):
        monitors = get_monitors()
        overlay = tk.Tk()
        monitor = monitors[self.config.monitor]
        overlay.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+0")

        overlay.attributes('-alpha', 0.8)#overlay transparency
        hwnd = int(overlay.winfo_id())
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, int(255 * 0.5), win32con.LWA_ALPHA)
        overlay.lift()
        overlay.focus_force()
        overlay.grab_set()
        overlay.grab_release()
        overlay.attributes("-topmost", True)

        image1 = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"assets","images","bonk.png"))
        test = ImageTk.PhotoImage(image1)

        bonk_image_label = tk.Label(image=test)
        bonk_image_label.image = test
        
        statistics = get_statistics_by_num_days(1)
        if len(statistics) > 0:
            (total_valid_time, total_invalid_time, date) = statistics[0]
            label = tk.Label(overlay, text= "Today you were sitting correctly for: "+str("{:.2f}".format(int(total_valid_time)))+" minutes", font=("Arial", 24), bg="white", fg="black", compound="top")
            label.place(relx=0.5, rely=0.1, anchor=tk.CENTER) 

        bonk_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER) 
        
        label = tk.Label(overlay, text=self.config.alarm_message, font=("Arial", 24), bg="white", fg="black", compound="top")
        label.place(relx=0.5, rely=0.6, anchor=tk.CENTER) 

        

        btn_15_min = tk.Button(overlay, text="Disable for 15 min", command=self.disable_for_15_min, font=("Arial", 24),  fg="green", bg="black")
        btn_15_min.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        btn_today = tk.Button(overlay, text="Disable for today", command=self.disable_for_today, font=("Arial", 24),  fg="green", bg="black")
        btn_today.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        overlay.after(300, self.updateStatus)

        return overlay
    
    def updateTimeStatistics(self, isPostureValid):
        if self.timer is not None:
            elapsed = (time.time_ns() - self.timer) / 1e9  # Convert nanoseconds to seconds
            if isPostureValid:
                self.valid_time+=elapsed
            else:
                self.invalid_time+=elapsed

            if self.valid_time > 60 or self.invalid_time > 60:
                     save_statistics_to_db(self.valid_time, self.invalid_time)
                     self.valid_time = 0
                     self.invalid_time = 0
        self.timer = time.time_ns()

    def wait_and_update_status(self, delay):
        timer_thread = threading.Timer(delay, self.updateStatus)
        timer_thread.daemon = True
        timer_thread.start()

    def updateStatus(self):
            if self.config.stop:
                return;
    
            show = self.show_overlay_function()
            self.updateTimeStatistics(not show)

            if show:
                if(self.invalid_position_consecutive_checks_seconds<self.config.alarm_delay):
                    self.invalid_position_consecutive_checks_seconds+=self.config.alarm_delay
                    if self.overlay is None:
                        self.wait_and_update_status(self.config.alarm_delay)
                    else:
                        self.overlay.after(300, self.updateStatus)
                    return
                self.invalid_position_consecutive_checks_seconds=0

            if self.disabledTimer > 0:
                overlay_to_destroy = self.overlay
                self.wait_and_update_status(self.disabledTimer)
                self.disabledTimer = 0
                if overlay_to_destroy is not None:
                    overlay_to_destroy.destroy()
                    self.overlay = None
            elif not show:
                overlay_to_destroy = self.overlay
                self.wait_and_update_status(self.config.alarm_delay)
                if overlay_to_destroy is not None:
                    overlay_to_destroy.destroy()
                    self.overlay = None
            elif self.overlay is None :
                self.overlay = self.create_overlay()
                self.overlay.mainloop()
            else:
                self.invalid_position_consecutive_checks_seconds=0
                self.overlay.after(300, self.updateStatus)

    def run(self):
        self.updateStatus()