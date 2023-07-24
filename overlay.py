import win32gui
import win32con
import tkinter as tk
import threading

overlay = tk.Tk()

def create_overlay(show_overlay_function):
    global overlay
    overlay = tk.Tk()
    overlay.attributes('-fullscreen', True)
    overlay.attributes('-alpha', 0.5)#overlay transparency
    hwnd = int(overlay.winfo_id())
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, int(255 * 0.5), win32con.LWA_ALPHA)

    label = tk.Label(overlay, text="Straighten up, ugly bastard!", font=("Arial", 24), bg="white", fg="black")
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER) 

    def updateStatus(show_overlay_function):
        global overlay
        show = show_overlay_function()
        if not show:
            overlay_to_destroy = overlay
            threading.Timer(1, updateStatus, [show_overlay_function]).start()
            if overlay_to_destroy is not None:
                overlay_to_destroy.destroy()
                overlay = None
        elif overlay is None:
            overlay = run(show_overlay_function)
        else:
            overlay.after(300, updateStatus, show_overlay_function)

    overlay.after(300, updateStatus, show_overlay_function)
    
    return overlay

def run(show_overlay_function):
    overlay = create_overlay(show_overlay_function)
    overlay.mainloop()




