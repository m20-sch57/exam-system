"""
Contains timer.
"""


from PyQt5 import Qt


class Timer:
    """
    Timer.
    """
    def __init__(self):
        self.current_time = -1
        self.timer_label = None

    def tie(self, timer_label):
        """
        Ties timer with timer_label.
        """
        self.timer_label = timer_label

    def untie(self):
        """
        Unties timer from timer_label.
        """
        self.timer_label = None

    def update(self, func):
        """
        Updates timer every second.
        """
        if self.current_time == 0:
            func()
            return
        self.current_time -= 1
        hours = self.current_time // 3600
        minutes = self.current_time % 3600 // 60
        seconds = self.current_time % 60
        try:
            self.timer_label.setText('%02d:%02d:%02d' % (hours, minutes, seconds))
            if self.current_time <= 10:
                self.timer_label.setStyleSheet('color: red')
            Qt.QTimer().singleShot(1000, lambda: self.update(func))
        except RuntimeError:
            return

    def start(self, duration, func):
        """
        Starts timer.
        """
        self.current_time = duration
        self.update(func)

    def reset(self):
        """
        Resets timer.
        """
        self.current_time = -1
        if self.timer_label is not None:
            self.timer_label.setText('')
            self.timer_label = None
