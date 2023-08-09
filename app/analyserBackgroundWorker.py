import threading
import datetime
from posture_analyser import PostureAnalyser
from shared_config import SharedConfig
import time
from db.db import save_statistics_to_db
from overlay import Overlay


class AnalyserBackgroundWorker:
    def __init__(self, shared_config: SharedConfig):
        self.config = shared_config
        self.disabledTimer = 0
        self.valid_time = 0
        self.invalid_time = 0
        self.timer = None
        self.invalid_position_consecutive_checks_seconds = 0
        self.overlay = Overlay(shared_config)
        self.analyzer = PostureAnalyser(shared_config)
        self.show_overlay_function = self.analyzer.calculate_if_show_overlay

    def disable_for_15_min(self):
        self.disabledTimer = 15 * 60

    def disable_for_today(self):
        def time_till_midnight():
            now = datetime.datetime.now()
            midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
            midnight = midnight + datetime.timedelta(days=1)
            time_remaining = midnight - now
            return time_remaining.total_seconds()

        self.disabledTimer = time_till_midnight()

    def updateTimeStatistics(self, isPostureValid):
        if self.timer is not None:
            elapsed = (time.time_ns() - self.timer) / \
                1e9  # Convert nanoseconds to seconds
            if isPostureValid:
                self.valid_time += elapsed
            else:
                self.invalid_time += elapsed

            if self.valid_time > 60 or self.invalid_time > 60:
                save_statistics_to_db(self.valid_time, self.invalid_time)
                self.valid_time = 0
                self.invalid_time = 0
        self.timer = time.time_ns()

    def wait_and_update_status(self, delay):
        timer_thread = threading.Timer(delay, self.updateStatus)
        timer_thread.daemon = True
        timer_thread.start()

    def updateStatus(self):
        if self.config.stop:
            return

        (show, frame) = self.show_overlay_function()
        self.updateTimeStatistics(not show)

        if show:
            self.overlay.frame = frame
            if (self.invalid_position_consecutive_checks_seconds < self.config.alarm_delay):
                self.invalid_position_consecutive_checks_seconds += self.config.alarm_delay/2
                if self.overlay.overlay is None:
                    self.wait_and_update_status(self.config.alarm_delay/2)
                else:
                    self.overlay.overlay.after(300, self.updateStatus)
                return
            self.invalid_position_consecutive_checks_seconds = 0

        if self.disabledTimer > 0:
            overlay_to_destroy = self.overlay.overlay
            self.wait_and_update_status(self.disabledTimer)
            self.disabledTimer = 0
            if overlay_to_destroy is not None:
                overlay_to_destroy.destroy()
                self.overlay.overlay = None
        elif not show:
            overlay_to_destroy = self.overlay.overlay
            self.wait_and_update_status(self.config.alarm_delay/2)
            if overlay_to_destroy is not None:
                overlay_to_destroy.destroy()
                self.overlay.overlay = None
        elif self.overlay.overlay is None:
            self.overlay.overlay = self.overlay.create_overlay(
                self.disable_for_15_min, self.disable_for_today, self.updateStatus)
            self.overlay.overlay.mainloop()
        else:
            self.invalid_position_consecutive_checks_seconds = 0
            self.overlay.overlay.after(300, self.updateStatus)

    def run(self):
        self.updateStatus()
