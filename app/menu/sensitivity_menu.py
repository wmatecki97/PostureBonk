import pystray
import tkinter as tk


class SensitivityMenu:
    def __init__(self, config):
        self.config = config
        self.menu = pystray.Menu(
            *self.get_sensitivity_menu()
        )

    def sensitivity_selected(self, icon, item):
        self.config.certainty = int(item.text[:-1])/100
        self.config.save_to_file()
        self.menu._items = tuple(self.get_sensitivity_menu())
        icon.update_menu()

    # to be replaced by a slider
    def get_sensitivity_menu(self):
        return [
            pystray.MenuItem("20%", self.sensitivity_selected,
                             enabled=(self.config.certainty != 0.2)),
            pystray.MenuItem("30%", self.sensitivity_selected,
                             enabled=(self.config.certainty != 0.3)),
            pystray.MenuItem("40%", self.sensitivity_selected,
                             enabled=(self.config.certainty != 0.4)),
            pystray.MenuItem("50%", self.sensitivity_selected,
                             enabled=(self.config.certainty != 0.5)),
            pystray.MenuItem("60%", self.sensitivity_selected,
                             enabled=(self.config.certainty != 0.6)),
            pystray.MenuItem("70%", self.sensitivity_selected,
                             enabled=(self.config.certainty != 0.7)),
            pystray.MenuItem("80%", self.sensitivity_selected,
                             enabled=(self.config.certainty != 0.8)),
            pystray.MenuItem("90%", self.sensitivity_selected,
                             enabled=(self.config.certainty != 0.9)),
            pystray.MenuItem("95%", self.sensitivity_selected, enabled=(self.config.certainty != 0.95))]
