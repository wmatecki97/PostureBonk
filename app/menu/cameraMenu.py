
from PIL import Image
import pystray
import tkinter as tk
import cv2
from screeninfo import get_monitors
import threading
import os


class CameraMenu:
    def __init__(self, config):
        self.config = config
        self.available_camera_indices = self.get_available_camera_indices()
        cameras_list = self.get_camera_menu()

        if len(self.available_camera_indices) > 1:
            self.menu = pystray.MenuItem("Camera", cameras_list)
        else:
            config.camera = 0
            self.menu = None

    def on_camera_selected(self, icon, camera_index):
        self.config.camera = int(str(camera_index))
        self.config.save_to_file()
        self.cameras_list._items = tuple(self.get_camera_menu())
        icon.update_menu()

    def get_camera_menu(self):
        return pystray.Menu(*[pystray.MenuItem(f"{index}", self.on_camera_selected, enabled=(self.config.camera != index)) for index in self.available_camera_indices])

    def get_available_camera_indices(self):
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
