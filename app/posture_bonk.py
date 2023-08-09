from PIL import Image
import pystray
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
from menu.sensitivity_menu import SensitivityMenu
from analyser_background_worker import AnalyserBackgroundWorker

image = Image.open(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'assets', 'images', 'icon.jpg'))

config = SharedConfig.create_from_file()

background_worker = AnalyserBackgroundWorker(config)
background_worker_thread = threading.Thread(
    target=background_worker.run)
background_worker_thread.daemon = True


def kill_current_app_and_create_new():
    global config
    global background_worker_thread
    global background_worker
    config.stop = True
    config = SharedConfig.create_from_file()
    background_worker = AnalyserBackgroundWorker(config)
    background_worker_thread = threading.Thread(
        target=background_worker.run)
    background_worker_thread.daemon = True
    background_worker_thread.start()


def exit_app(icon):
    config.stop = True
    icon.stop()


camera_menu = CameraMenu(config)
monitor_menu = MonitorMenu(config)
alarm_delay_menu = AlarmDelayMenu(config, kill_current_app_and_create_new)
sensitivity_menu = SensitivityMenu(config)
alarm_dialog = AlarmMessageDialog(config)

menu_items = [item for item in [
    camera_menu.menu,
    monitor_menu.menu,
    pystray.MenuItem("Resume", kill_current_app_and_create_new),
    pystray.MenuItem("Change alarm message",
                     alarm_dialog.show_alarm_message_dialog),
    pystray.MenuItem("Sensitivity", sensitivity_menu.menu),
    pystray.MenuItem("Alarm after", alarm_delay_menu.menu),
    pystray.MenuItem("Statistics", show_statistics_chart_window),
    pystray.MenuItem("Exit", exit_app)] if item is not None]

icon = pystray.Icon("Neural", image, menu=pystray.Menu(
    *menu_items
))

background_worker_thread.start()
icon.run()
