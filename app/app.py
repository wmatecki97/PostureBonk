from PIL import Image
import pystray
import tkinter as tk
from shared_config import SharedConfig
from PIL import Image
from posture_analyser import PostureAnalyser
import cv2
from screeninfo import get_monitors
import threading
import os 

image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'images', 'icon.jpg'))
config = SharedConfig.create_from_file()
posture_analyser_instance = PostureAnalyser(config)
posture_analyser_thread = threading.Thread(target=posture_analyser_instance.run)
posture_analyser_thread.daemon = True

def kill_current_app_and_create_new():
    global config
    global posture_analyser_thread
    global posture_analyser_instance
    config.stop = True
    config = SharedConfig.create_from_file()
    posture_analyser_instance = PostureAnalyser(config)
    posture_analyser_thread = threading.Thread(target=posture_analyser_instance.run)
    posture_analyser_thread.daemon = True
    posture_analyser_thread.start()


def exit_app(icon):
    icon.stop()

def show_alarm_message_dialog(icon, item):
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
    certainty_menu._items = tuple(get_certainty_menu())
    icon.update_menu()

def delay_selected(icon, item):
    global config
    config.alarm_delay = int(item.text[:-1])
    config.save_to_file()
    alarm_delay_menu._items = tuple(get_alarm_delay_menu())
    icon.update_menu()
    kill_current_app_and_create_new()

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
    global config
    config.camera = int(str(camera_index))
    config.save_to_file()
    cameras_list._items = tuple(get_camera_menu())
    icon.update_menu()

def on_monitor_selected(icon, monitor_index):
    global config
    config.monitor = int(str(monitor_index))
    config.save_to_file()
    monitors_list._items = tuple(get_monitor_menu())
    icon.update_menu()

# Get available camera indices
available_camera_indices = get_available_camera_indices()
def get_camera_menu():
    global config
    return pystray.Menu(*[pystray.MenuItem(f"{index}", on_camera_selected, enabled=(config.camera != index)) for index in available_camera_indices])
cameras_list = get_camera_menu()
if len(available_camera_indices) > 1:
    camera_menu = pystray.MenuItem("Camera", cameras_list)
else:
    camera_menu = None

monitors = get_monitors()
def get_monitor_menu():
    global config
    return pystray.Menu(*[pystray.MenuItem(f"{i}", on_monitor_selected, enabled=(config.monitor != i)) for i in range(len(monitors))])

monitors_list = get_monitor_menu()

if len(monitors_list.items) > 1:
    monitor_menu = pystray.MenuItem("Monitor", monitors_list)
else:
    monitor_menu = None

def get_certainty_menu():
    return[
    pystray.MenuItem("20%", certainty_selected, enabled=(config.certainty != 0.2)),
    pystray.MenuItem("30%", certainty_selected, enabled=(config.certainty != 0.3)),
    pystray.MenuItem("40%", certainty_selected, enabled=(config.certainty != 0.4)),
    pystray.MenuItem("50%", certainty_selected, enabled=(config.certainty != 0.5)),
    pystray.MenuItem("60%", certainty_selected, enabled=(config.certainty != 0.6)),
    pystray.MenuItem("70%", certainty_selected, enabled=(config.certainty != 0.7)),
    pystray.MenuItem("80%", certainty_selected, enabled=(config.certainty != 0.8)),
    pystray.MenuItem("90%", certainty_selected, enabled=(config.certainty != 0.9)),
    pystray.MenuItem("95%", certainty_selected, enabled=(config.certainty != 0.95))]

certainty_menu = pystray.Menu(
  *get_certainty_menu()
)

def get_alarm_delay_menu():
    return [pystray.MenuItem("1s", delay_selected,  enabled=(config.alarm_delay != 1)),
    pystray.MenuItem("3s", delay_selected, enabled=(config.alarm_delay != 3)),
    pystray.MenuItem("5s", delay_selected, enabled=(config.alarm_delay != 5)),
    pystray.MenuItem("10s", delay_selected, enabled=(config.alarm_delay != 10)),
    pystray.MenuItem("30s", delay_selected, enabled=(config.alarm_delay != 30))]

alarm_delay_menu = pystray.Menu(
    *get_alarm_delay_menu()
)

menu_items = [ item for item in [
    camera_menu,   
    monitor_menu, 
    pystray.MenuItem("Resume", kill_current_app_and_create_new),
    #pystray.MenuItem("Stop for 15 min", exit_app),
    #pystray.MenuItem("Stop for today", show_alarm_message_dialog),
    pystray.MenuItem("Change alarm message", show_alarm_message_dialog),
    pystray.MenuItem("Certainty", certainty_menu),
    pystray.MenuItem("Alarm after", alarm_delay_menu),
    pystray.MenuItem("Exit", exit_app)] if item is not None]

icon = pystray.Icon("Neural", image, menu=pystray.Menu(
*menu_items
))


posture_analyser_thread.start()

icon.run()
