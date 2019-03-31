"""
Contains all widgets for exam status.
"""


from time import time
from PyQt5 import Qt
from timer import Timer


class ExamRunning(Qt.QWidget):
    """
    Returns widget for running exam.
    """
    def __init__(self, app, parent):
        super().__init__()
        exam_data = parent.exam_data

        finish_button = Qt.QPushButton('Закончить экзамен', self)
        finish_button.setObjectName('Button')
        finish_button.setFont(Qt.QFont('Arial', 20))
        finish_button.clicked.connect(lambda: app.finish_exam(exam_data['rowid']))

        info_str = (
            ' Всего баллов: ' + str(exam_data['total_score']) +
            ' (из ' + str(exam_data['total_maxscore']) + ')'
        )

        info_label = Qt.QLabel(info_str, self)
        info_label.setFont(Qt.QFont('Arial', 20))

        timer_label = Qt.QLabel(self)
        timer_label.setFont(Qt.QFont('Arial', 25))

        timer = Timer()
        timer.tie(timer_label)
        timer.start(exam_data['end'] - int(time()), lambda: app.finish_exam(exam_data['rowid']))

        status_layout = Qt.QHBoxLayout()
        status_layout.addWidget(finish_button)
        status_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        status_layout.addWidget(info_label)
        status_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        status_layout.addStretch(1)
        status_layout.addWidget(timer_label)
        self.setLayout(status_layout)


class ExamFinished(Qt.QWidget):
    """
    Contains widget for finished exam.
    """
    def __init__(self, parent):
        super().__init__()
        exam_data = parent.exam_data
        info_str = (
            'Экзамен завершён. Суммарный балл - ' +
            str(exam_data['total_score']) + ' (из ' +
            str(exam_data['total_maxscore']) + ')'
        )

        info_label = Qt.QLabel(info_str, self)
        info_label.setFont(Qt.QFont('Arial', 25))
        info_label.setWordWrap(True)

        status_layout = Qt.QHBoxLayout()
        status_layout.addWidget(info_label)
        self.setLayout(status_layout)
