import threading
import datetime
from posture_analyser import PostureAnalyser
from shared_config import SharedConfig
import time
from db.db import save_statistics_to_db
from overlay import Overlay
import math


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

    def update_time_statistics(self, isPostureValid):
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

    def main_loop(self):
        delay = 0
        while True:
            if self.config.stop:
                return
            else:
                time.sleep(delay)

            (show, frame) = self.show_overlay_function(
                self.overlay.overlay is None)

            self.update_time_statistics(not show)

            if show:
                self.overlay.frame = frame
                if (self.invalid_position_consecutive_checks_seconds < self.config.alarm_delay):
                    self.invalid_position_consecutive_checks_seconds += math.ceil(
                        self.config.alarm_delay/2.0)
                    if self.overlay.overlay is None:
                        delay = self.config.alarm_delay/2
                    else:
                        delay = 0.3
                self.invalid_position_consecutive_checks_seconds = 0

            if self.disabledTimer > 0:
                overlay_to_destroy = self.overlay.overlay
                delay = self.disabledTimer
                self.disabledTimer = 0
                if overlay_to_destroy is not None:
                    overlay_to_destroy.destroy()
                    self.overlay.overlay = None
            elif not show:
                overlay_to_destroy = self.overlay.overlay
                delay = self.config.alarm_delay/2
                if overlay_to_destroy is not None:
                    overlay_to_destroy.destroy()
                    self.overlay.overlay = None
            elif self.overlay.overlay is None:
                self.overlay.overlay = self.overlay.create_overlay(
                    self.disable_for_15_min, self.disable_for_today, self.main_loop)
                self.overlay.overlay.mainloop()
            else:
                self.invalid_position_consecutive_checks_seconds = 0

    def run(self):
        self.main_loop()
