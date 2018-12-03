"""
Page before starting the exam.
"""


import os
from PyQt5.Qt import Qt, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.Qt import QLabel, QPushButton
from PyQt5.Qt import QFont, QPixmap, QSize, QSpacerItem
from mywidgets import Pixmap


class StartExamPage(QWidget):
    """
    Page before starting the exam.
    """
    def __init__(self, exam, exam_info, back_function, start_function):
        super().__init__()
        info_str = (
            'Информация об экзамене:\n\n'
            '    Продолжительность - ' + str(exam_info['duration']) + ' минут\n' +
            '    Количество заданий - ' + str(exam_info['quantity']) + '\n\n' +
            'Прервать выполнение заданий будет невозможно.\n'
            'Вы уверены, что хотите начать экзамен?')

        back_img = Pixmap(normal_pic=QPixmap(os.path.join('images', 'left-50x50.png')),
                          hover_pic=QPixmap(os.path.join('images', 'left-50x50.png')))
        back_img.setFixedSize(QSize(50, 50))
        back_img.clicked.connect(back_function)

        exam_title = QLabel(exam)
        exam_title.setFont(QFont('Arial', 30))
        exam_title.setAlignment(Qt.AlignCenter)
        exam_title.setWordWrap(True)

        info_label = QLabel(info_str)
        info_label.setFont(QFont('Arial', 20))
        info_label.setWordWrap(True)

        start_button = QPushButton('Начать экзамен')
        start_button.setFont(QFont('Arial', 20))
        start_button.setMinimumSize(QSize(250, 50))
        start_button.clicked.connect(lambda: start_function(exam))

        upper_layout = QHBoxLayout()
        upper_layout.addWidget(back_img)
        upper_layout.addWidget(exam_title)

        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(30, 0))
        button_layout.addWidget(start_button)
        button_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(QSpacerItem(0, 20))
        layout.addWidget(info_label)
        layout.addSpacerItem(QSpacerItem(0, 30))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)
