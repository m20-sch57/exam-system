"""
Page before starting the exam.
"""


from PyQt5 import Qt
from mywidgets import Pixmap
import common


class StartExamPage(Qt.QWidget):
    """
    Page before starting the exam.
    """
    def __init__(self, exam, exam_info, back_function, start_function):
        super().__init__()
        info_str = (
            'Информация об экзамене:\n\n'
            'Продолжительность - ' + str(exam_info['duration']) + ' минут\n' +
            'Количество заданий - ' + str(exam_info['quantity'])
        )

        back_img = Pixmap(normal_pic=Qt.QPixmap(common.LEFT50),
                          hover_pic=Qt.QPixmap(common.LEFT50))
        back_img.setFixedSize(Qt.QSize(50, 50))
        back_img.clicked.connect(back_function)

        exam_title = Qt.QLabel(exam)
        exam_title.setFont(Qt.QFont('Arial', 30))
        exam_title.setAlignment(Qt.Qt.AlignCenter)
        exam_title.setWordWrap(True)

        info_label = Qt.QLabel(info_str)
        info_label.setFont(Qt.QFont('Arial', 20))
        info_label.setWordWrap(True)

        start_button = Qt.QPushButton('Начать экзамен')
        start_button.setFont(Qt.QFont('Arial', 20))
        start_button.setMinimumSize(Qt.QSize(240, 50))
        start_button.clicked.connect(lambda: start_function(exam))

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_img)
        upper_layout.addWidget(exam_title)

        button_layout = Qt.QHBoxLayout()
        button_layout.addSpacerItem(Qt.QSpacerItem(30, 0))
        button_layout.addWidget(start_button)
        button_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(info_label)
        layout.addSpacerItem(Qt.QSpacerItem(0, 30))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)
