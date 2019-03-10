"""
Student's home page with list of exams.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class HomePage(Qt.QWidget):
    """
    Student's home page with list of exams.
    """
    def __init__(self, app):
        super().__init__()
        list_of_exams = app.list_of_exams()

        exams_title = Qt.QLabel('Доступные экзамены')
        exams_title.setFont(Qt.QFont('Arial', 30))

        exit_button = FlatButton(Qt.QIcon(common.USER), '')
        exit_button.setIconSize(Qt.QSize(40, 40))
        exit_button.clicked.connect(lambda _: app.logout())

        scroll_area = Qt.QScrollArea()
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.setSizeConstraint(Qt.QLayout.SetMinimumSize)

        for exam in list_of_exams:
            exam_id = exam['rowid']
            exam_name = exam['name']

            exam_button = FlatButton(Qt.QIcon(common.EXAM30), exam_name)
            exam_button.setIconSize(Qt.QSize(30, 30))
            exam_button.setFont(Qt.QFont('Arial', 20))
            exam_button.clicked.connect(common.return_lambda(app.display_exam, exam_id))

            exam_layout = Qt.QHBoxLayout()
            exam_layout.addWidget(exam_button)
            exam_layout.addStretch(1)

            scroll_layout.addLayout(exam_layout)
            scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))

        scroll_layout.addStretch(1)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addStretch(1)
        upper_layout.addWidget(exams_title)
        upper_layout.addStretch(1)
        upper_layout.addWidget(exit_button)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(scroll_area)
        self.setLayout(layout)
