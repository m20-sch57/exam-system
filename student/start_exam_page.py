"""
Page before starting the exam.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class StartExamPage(Qt.QWidget):
    """
    Page before starting the exam.
    """
    def __init__(self, app, exam_data, cnt_questions):
        super().__init__()
        info_str = (
            'Продолжительность - ' + str(exam_data['duration']) + ' минут\n' +
            'Количество заданий - ' + str(cnt_questions)
        )

        back_button = FlatButton(Qt.QIcon(common.LEFT), '')
        back_button.setIconSize(Qt.QSize(40, 40))
        back_button.setFixedSize(back_button.sizeHint())
        back_button.clicked.connect(app.display_home_page)

        exam_title = Qt.QLabel(exam_data['name'])
        exam_title.setFont(Qt.QFont('Arial', 30))
        exam_title.setAlignment(Qt.Qt.AlignCenter)
        exam_title.setWordWrap(True)

        info_title = Qt.QLabel('Информация')
        info_title.setFont(Qt.QFont('Arial', 25))

        info_label = Qt.QLabel(info_str)
        info_label.setFont(Qt.QFont('Arial', 20))
        info_label.setWordWrap(True)

        start_button = Qt.QPushButton('Начать экзамен')
        start_button.setFont(Qt.QFont('Arial', 20))
        start_button.clicked.connect(lambda: app.start_exam(exam_data['rowid']))

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addWidget(exam_title)

        info_layout = Qt.QHBoxLayout()
        info_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        info_layout.addWidget(info_label)

        button_layout = Qt.QHBoxLayout()
        button_layout.addWidget(start_button)
        button_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        layout.addWidget(info_title)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(info_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 30))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)
