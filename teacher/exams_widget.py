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
    def __init__(self, app):
        super().__init__()
        list_of_exams = app.list_of_exams()

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

        create_button = FlatButton(Qt.QIcon(common.CREATE), 'Создать экзамен')
        create_button.setIconSize(Qt.QSize(40, 40))
        create_button.setFont(Qt.QFont('Arial', 20))
        create_button.clicked.connect(lambda _: app.create_exam())

        info_label = Qt.QLabel('Всего экзаменов - ' + str(len(list_of_exams)))
        info_label.setFont(Qt.QFont('Arial', 20))

        lower_layout = Qt.QHBoxLayout()
        lower_layout.addWidget(create_button)
        lower_layout.addStretch(1)
        lower_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        lower_layout.addWidget(info_label)
        lower_layout.addSpacerItem(Qt.QSpacerItem(10, 0))

        layout = Qt.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(lower_layout)
        self.setLayout(layout)
