from PIL import Image
import pystray
from menu.sensitivity_settings import SensitivitySettings
from shared_config import SharedConfig
from PIL import Image
from posture_analyser import PostureAnalyser
import threading
import os
from menu.statistic_chart import show_statistics_chart_window
from menu.alarm_message_dialog import AlarmMessageDialog
from menu.camera_menu import CameraMenu
from menu.monitor_menu import MonitorMenu
from menu.alarm_delay_menu import AlarmDelayMenu
from analyser_background_worker import AnalyserBackgroundWorker

image = Image.open(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'assets', 'images', 'icon.jpg'))

config = SharedConfig.create_from_file()

background_worker_thread = None

def kill_current_app_and_create_new():
    kill_current_worker()
    start_new_worker()


def start_new_worker():
    global background_worker_thread
    background_worker = AnalyserBackgroundWorker(config)
    background_worker_thread = threading.Thread(
        target=background_worker.run)
    background_worker_thread.daemon = True
    background_worker_thread.start()


def kill_current_worker():
    global config
    config.stop = True
    config = SharedConfig.create_from_file()


def exit_app(icon):
    global config
    global background_worker_thread
    PostureAnalyser.release()
    
    config.stop = True
    background_worker_thread.join()
    icon.stop()


def change_sensitivity_settings():
    kill_current_worker()
    sensitivity_menu = SensitivitySettings(config, start_new_worker)
    sensitivity_menu.show()


camera_menu = CameraMenu(config)
monitor_menu = MonitorMenu(config)
alarm_delay_menu = AlarmDelayMenu(config, kill_current_app_and_create_new)
alarm_dialog = AlarmMessageDialog(config)

menu_items = [item for item in [
    camera_menu.menu,
    monitor_menu.menu,
    pystray.MenuItem("Resume", kill_current_app_and_create_new),
    pystray.MenuItem("Change alarm message",
                     alarm_dialog.show_alarm_message_dialog),
    pystray.MenuItem("Sensitivity", change_sensitivity_settings),
    pystray.MenuItem("Alarm after", alarm_delay_menu.menu),
    pystray.MenuItem("Statistics", show_statistics_chart_window),
    pystray.MenuItem("Exit", exit_app)] if item is not None]

icon = pystray.Icon("Neural", image, menu=pystray.Menu(
    *menu_items
))

change_sensitivity_settings()
icon.run()
