"""
Widget for home page with list of exams.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class ExamsWidget(Qt.QWidget):
    """
    Widget for home page with list of exams.
    """
    def __init__(self, user, list_of_exams, exam_function):
        super().__init__()

        scroll_area = Qt.QScrollArea()
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.setSizeConstraint(Qt.QLayout.SetMinimumSize)

        for exam in list_of_exams:
            exam_checkbox = Qt.QCheckBox()

            exam_button = FlatButton(Qt.QIcon(common.EXAM30), exam)
            exam_button.setFont(Qt.QFont('Arial', 20))
            exam_button.setIconSize(Qt.QSize(30, 30))
            exam_button.clicked.connect(common.return_lambda(exam_function, exam))

            exam_layout = Qt.QHBoxLayout()
            exam_layout.addWidget(exam_checkbox)
            exam_layout.addWidget(exam_button)
            exam_layout.addStretch(1)

            scroll_layout.addLayout(exam_layout)
            scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))

        scroll_layout.addStretch(1)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        add_button = FlatButton('Добавить')
        add_button.setFont(Qt.QFont('Arial', 20))

        remove_button = FlatButton('Удалить')
        remove_button.setFont(Qt.QFont('Arial', 20))

        lower_layout = Qt.QHBoxLayout()
        lower_layout.addWidget(add_button)
        lower_layout.addStretch(1)
        lower_layout.addWidget(remove_button)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(lower_layout)
        self.setLayout(layout)
