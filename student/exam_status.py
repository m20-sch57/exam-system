"""
Contains all widgets for exam status.
"""


import time
from PyQt5 import Qt
from mywidgets import Timer


class ExamRunning(Qt.QWidget):
    """
    Returns widget for running exam.
    """
    def __init__(self, parent, finish_function):
        super().__init__()

        info_label = Qt.QLabel('Экзамен идёт.')
        info_label.setFont(Qt.QFont('Arial', 25))

        timer_label = Qt.QLabel()
        timer_label.setFont(Qt.QFont('Arial', 25))
        timer = Timer()
        timer.tie(timer_label)
        timer.start(int(parent.exam_info['end']) - int(time.time()),
                    lambda: finish_function(parent.exam))

        status_layout = Qt.QHBoxLayout()
        status_layout.addWidget(info_label)
        status_layout.addStretch(1)
        status_layout.addWidget(timer_label)
        self.setLayout(status_layout)


class ExamFinished(Qt.QWidget):
    """
    Contains widget for finished exam.
    """
    def __init__(self, parent):
        super().__init__()
        total_score = parent.exam_info['total_score']
        total_maxscore = parent.exam_info['total_maxscore']

        info_label = Qt.QLabel(
            'Экзамен завершён. Суммарный балл - ' +
            str(total_score) + ' (из ' + str(total_maxscore) + ')')
        info_label.setFont(Qt.QFont('Arial', 25))
        info_label.setWordWrap(True)

        status_layout = Qt.QHBoxLayout()
        status_layout.addWidget(info_label)
        self.setLayout(status_layout)
