import tkinter as tk


class AlarmMessageDialog:
    def __init__(self, config):
        self.config = config

    def show_alarm_message_dialog(self, icon, item):
        config = self.config

        class InputDialog(tk.Toplevel):
            def __init__(self, parent, title):
                super().__init__(parent)
                self.title(title)
                self.geometry("300x100")

                self.label = tk.Label(self, text="Enter your alarm message:")
                self.label.pack()

                self.entry = tk.Entry(self)
                self.entry.insert(0, config.alarm_message)
                self.entry.pack()

                self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
                self.ok_button.pack()

            def on_ok(self):
                self.user_input = self.entry.get()
                self.destroy()

        root = tk.Tk()
        root.withdraw()

        input_dialog = InputDialog(root, "User Input")
        root.wait_window(input_dialog)

        self.config.alarm_message = input_dialog.user_input
        self.config.save_to_file()

        root.destroy()
