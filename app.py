from PIL import Image
import pystray
from tkinter import simpledialog, Tk, Toplevel
import tkinter as tk
from shared_config import SharedConfig
from PIL import Image
from posture_analyser import PostureAnalyser
from threading import Thread
import cv2
from screeninfo import get_monitors
import threading

image = Image.open("icon.jpg")
config = SharedConfig.create_from_file()

def exit_app(icon):
    icon.stop()

def show_input_dialog(icon, item):
    global config 
    class InputDialog(tk.Toplevel):
        def __init__(self, parent, title):
            super().__init__(parent)
            self.title(title)
            self.geometry("300x100")

            self.label = tk.Label(self, text="Enter your alarm message:")
            self.label.pack()

            self.entry = tk.Entry(self)
            self.entry.insert(0,config.alarm_message)
            self.entry.pack()

            self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
            self.ok_button.pack()

        def on_ok(self):
            self.user_input = self.entry.get()
            self.destroy()

    root = tk.Tk()  
    root.withdraw()  # Hide the root window

    input_dialog = InputDialog(root, "User Input")
    root.wait_window(input_dialog) 

    config.alarm_message = input_dialog.user_input
    config.save_to_file()

    root.destroy()  # Destroy the root window

def certainty_selected(icon, item):
    global config
    config.certainty = int(item.text[:-1])/100
    config.save_to_file()

def get_available_camera_indices():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

def on_camera_selected(icon, camera_index):
    config.camera = int(str(camera_index))
    config.save_to_file()

def on_monitor_selected(icon, monitor_index):
    print(monitor_index)
    config.monitor = int(str(monitor_index))
    config.save_to_file()

# Get available camera indices
available_camera_indices = get_available_camera_indices()
camera_list = pystray.Menu(*[pystray.MenuItem(f"{index}", on_camera_selected) for index in available_camera_indices])
if len(available_camera_indices) > 1:
    camera_menu = pystray.MenuItem("Camera", camera_list)
else:
    camera_menu = None

monitors = get_monitors()
monitors_list = pystray.Menu(*[pystray.MenuItem(f"{i}", on_monitor_selected) for i in range(len(available_camera_indices)+1)])
if len(monitors) > 1:
    monitor_menu = pystray.MenuItem("Monitor", monitors_list)
else:
    monitor_menu = None

certainty_menu = pystray.Menu(
    pystray.MenuItem("50%", certainty_selected),
    pystray.MenuItem("60%", certainty_selected),
    pystray.MenuItem("70%", certainty_selected),
    pystray.MenuItem("80%", certainty_selected),
    pystray.MenuItem("90%", certainty_selected),
    pystray.MenuItem("95%", certainty_selected),
)

menu_items = [ item for item in [
    camera_menu,   
    monitor_menu, 
    pystray.MenuItem("Start", exit_app),
    pystray.MenuItem("Stop for 15 min", exit_app),
    pystray.MenuItem("Stop for today min", show_input_dialog),
    pystray.MenuItem("Certainty", certainty_menu),
    pystray.MenuItem("Exit", exit_app)] if item is not None]

icon = pystray.Icon("Neural", image, menu=pystray.Menu(
*menu_items
))

posture_analyser_instance = PostureAnalyser(config)
timer_thread = threading.Thread(target=posture_analyser_instance.run)
timer_thread.daemon = True
timer_thread.start()

icon.run()
