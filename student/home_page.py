"""
Student's home page with list of exams.
"""


import os
from PyQt5.Qt import Qt, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.Qt import QLabel, QScrollArea
from PyQt5.Qt import QFont, QPixmap, QSize, QSpacerItem, QFrame
from mywidgets import Label


class HomePage(QWidget):
    """
    Student's home page with list of exams.
    """
    def __init__(self, user, list_of_exams, exam_function):
        super().__init__()

        group_title = QLabel('Группа ' + user.group)
        group_title.setFont(QFont('Arial', 30))
        group_title.setAlignment(Qt.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        scroll_layout = QVBoxLayout()

        for exam in list_of_exams:
            exam_image = QLabel()
            exam_image.setPixmap(QPixmap(os.path.join('data', 'exam-30x30.png')))
            exam_image.setFixedSize(QSize(30, 30))

            exam_label = Label(exam, normal_color='black', hover_color='blue')
            exam_label.setFont(QFont('Arial', 20))
            exam_label.setWordWrap(True)
            exam_label.connect(exam_function, exam)

            exam_layout = QHBoxLayout()
            exam_layout.addWidget(exam_image)
            exam_layout.addWidget(exam_label)

            scroll_layout.addLayout(exam_layout)
            scroll_layout.addSpacerItem(QSpacerItem(0, 10))

        scroll_layout.addStretch(1)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout()
        layout.addWidget(group_title)
        layout.addSpacerItem(QSpacerItem(0, 20))
        layout.addWidget(scroll_area)
        self.setLayout(layout)
