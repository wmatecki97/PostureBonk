import win32gui
import win32con
import tkinter as tk


show = True

# Function to create a transparent overlay window covering the whole screen
def create_overlay():
    # Create a transparent toplevel window
    overlay = tk.Tk()
    overlay.attributes('-fullscreen', True)
    overlay.attributes('-alpha', 0.5)  # Adjust the alpha value to control transparency (0.0 to 1.0)

    # Set the window at the topmost layer to act as an overlay
    hwnd = int(overlay.winfo_id())
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, int(255 * 0.5), win32con.LWA_ALPHA)

    # Create a label widget to display the text
    label = tk.Label(overlay, text="Straighten up, ugly bastard!", font=("Arial", 24), bg="white", fg="black")
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place the label at the center of the overlay

    overlay.after(300, overlay.destroy)
    
    return overlay

def run():
    # Create the overlay
    overlay = create_overlay()

    # Start the tkinter main loop
    overlay.mainloop()

run()


