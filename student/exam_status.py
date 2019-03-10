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
    def __init__(self, app, exam_data):
        super().__init__()

        finish_button = Qt.QPushButton('Закончить экзамен')
        finish_button.setFont(Qt.QFont('Arial', 20))
        finish_button.clicked.connect(lambda: app.finish_exam(exam_data['rowid']))

        timer_label = Qt.QLabel()
        timer_label.setFont(Qt.QFont('Arial', 25))
        timer = Timer()
        timer.tie(timer_label)
        timer.start(exam_data['end'] - int(time.time()),
                    lambda: app.finish_exam(exam_data['rowid']))

        status_layout = Qt.QHBoxLayout()
        status_layout.addWidget(finish_button)
        status_layout.addStretch(1)
        status_layout.addWidget(timer_label)
        self.setLayout(status_layout)


class ExamFinished(Qt.QWidget):
    """
    Contains widget for finished exam.
    """
    def __init__(self, exam_data):
        super().__init__()
        info_str = (
            'Экзамен завершён. Суммарный балл - ' +
            str(exam_data['total_score']) + ' (из ' +
            str(exam_data['total_maxscore']) + ')'
        )

        info_label = Qt.QLabel(info_str)
        info_label.setFont(Qt.QFont('Arial', 25))
        info_label.setWordWrap(True)

        status_layout = Qt.QHBoxLayout()
        status_layout.addWidget(info_label)
        self.setLayout(status_layout)
