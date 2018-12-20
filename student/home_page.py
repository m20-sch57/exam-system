"""
Student's home page with list of exams.
"""


from PyQt5 import Qt
from mywidgets import Label
import common


class HomePage(Qt.QWidget):
    """
    Student's home page with list of exams.
    """
    def __init__(self, user, list_of_exams, exam_function):
        super().__init__()

        group_title = Qt.QLabel('Группа ' + user.group)
        group_title.setFont(Qt.QFont('Arial', 30))
        group_title.setAlignment(Qt.Qt.AlignCenter)

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        scroll_layout = Qt.QVBoxLayout()

        for exam in list_of_exams:
            exam_image = Qt.QLabel()
            exam_image.setPixmap(Qt.QPixmap(common.EXAM30))
            exam_image.setFixedSize(Qt.QSize(30, 30))

            exam_label = Label(exam, normal_color='black', hover_color='blue')
            exam_label.setFont(Qt.QFont('Arial', 20))
            exam_label.setWordWrap(True)
            exam_label.connect(exam_function, exam)

            exam_layout = Qt.QHBoxLayout()
            exam_layout.addWidget(exam_image)
            exam_layout.addWidget(exam_label)

            scroll_layout.addLayout(exam_layout)
            scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))

        scroll_layout.addStretch(1)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(group_title)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(scroll_area)
        self.setLayout(layout)
