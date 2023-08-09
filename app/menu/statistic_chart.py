import tkinter as tk
import threading
from db.db import get_statistics_by_num_days
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates


def plot_statistics_chart():
    num_days = 30
    stats = get_statistics_by_num_days(num_days)

    valid_times, invalid_times, dates = zip(*stats)

    fig, ax = plt.subplots()
    ax.plot(dates, valid_times, label='Valid Time')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    ax.set_xlabel('Days')
    ax.set_ylabel('Total Time (minutes)')
    ax.set_title('Statistics of the Last 30 Days')
    ax.legend()

    root = tk.Tk()
    root.title('Statistics Chart')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def close_window():
        plt.close(fig)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_window)
    root.mainloop()


def show_statistics_chart_window():
    t = threading.Thread(target=plot_statistics_chart)
    t.daemon = True
    t.start()
