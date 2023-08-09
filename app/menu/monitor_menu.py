
from PIL import Image
import pystray
import tkinter as tk
import cv2
from screeninfo import get_monitors
import threading
import os


class MonitorMenu:
    def __init__(self, config):
        self.config = config
        self.monitors = get_monitors()
        monitors_list = self.get_monitor_menu()

        if len(monitors_list.items) > 1:
            self.menu = pystray.MenuItem("Monitor", monitors_list)
        else:
            config.monitor = 0
            self.menu = None

    def get_monitor_menu(self):
        return pystray.Menu(*[pystray.MenuItem(f"{i}", self.on_monitor_selected, enabled=(self.config.monitor != i)) for i in range(len(self.monitors))])

    def on_monitor_selected(self, icon, monitor_index):
        self.config.monitor = int(str(monitor_index))
        self.config.save_to_file()
        self.monitors_list._items = tuple(self.get_monitor_menu())
        icon.update_menu()
