import pystray
import tkinter as tk


class AlarmDelayMenu:
    def __init__(self, config, kill_current_app_and_create_new):
        self.config = config
        self.kill_current_app_and_create_new = kill_current_app_and_create_new
        self.menu = pystray.Menu(
            *self.get_alarm_delay_menu()
        )

    def delay_selected(self, icon, item):
        self.config.alarm_delay = int(item.text[:-1])
        self.config.save_to_file()
        self.menu._items = tuple(self.get_alarm_delay_menu())
        icon.update_menu()
        self.kill_current_app_and_create_new()

    def get_alarm_delay_menu(self):
        return [pystray.MenuItem("1s", self.delay_selected,  enabled=(self.config.alarm_delay != 1)),
                pystray.MenuItem("3s", self.delay_selected,
                                 enabled=(self.config.alarm_delay != 3)),
                pystray.MenuItem("5s", self.delay_selected,
                                 enabled=(self.config.alarm_delay != 5)),
                pystray.MenuItem("10s", self.delay_selected,
                                 enabled=(self.config.alarm_delay != 10)),
                pystray.MenuItem("30s", self.delay_selected, enabled=(self.config.alarm_delay != 30))]
