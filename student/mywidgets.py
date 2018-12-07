"""
Contains my widgets.
"""

from PyQt5.Qt import Qt, QLabel, QPixmap, pyqtSignal, QTimer


class Label(QLabel):
    """
    Link with text.
    """
    clicked = pyqtSignal()
    def __init__(self, text, normal_color=None, hover_color=None):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.mousePressEvent = lambda event: self.clicked.emit()
        if normal_color is not None:
            self.setStyleSheet('color: ' + normal_color)
            self.leaveEvent = lambda event: self.setStyleSheet('color: ' + self.normal_color)
        if hover_color is not None:
            self.enterEvent = lambda event: self.setStyleSheet('color: ' + self.hover_color)

    def connect(self, function, *args, **kwargs):
        """
        Connects mouse press event to the function.
        """
        self.clicked.connect(lambda: function(*args, **kwargs))


class Pixmap(QLabel):
    """
    Link with image.
    """
    clicked = pyqtSignal()
    def __init__(self, normal_pic, hover_pic):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)
        self.setPixmap(QPixmap(normal_pic))
        self.normal_pic = normal_pic
        self.hover_pic = hover_pic
        self.mousePressEvent = lambda event: self.clicked.emit()
        self.enterEvent = lambda event: self.setPixmap(self.hover_pic)
        self.leaveEvent = lambda event: self.setPixmap(self.normal_pic)

    def connect(self, function):
        """
        Connects mouse press event to the function.
        """
        self.clicked.connect(function)


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
            QTimer().singleShot(1000, lambda: self.update(func))
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
