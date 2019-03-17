"""
Student's home page with list of exams.
"""


from PyQt5 import Qt
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

        view_profile_action = Qt.QWidgetAction(self)
        view_profile_action.setFont(Qt.QFont('Arial', 15))
        view_profile_action.setText('Профиль')
        view_profile_action.triggered.connect(lambda _: app.logout())

        exit_action = Qt.QWidgetAction(self)
        exit_action.setFont(Qt.QFont('Arial', 15))
        exit_action.setText('Выйти')
        exit_action.triggered.connect(lambda _: app.logout())

        user_menu = Qt.QMenu(self)
        user_menu.addAction(view_profile_action)
        user_menu.addAction(exit_action)

        user_button = Qt.QPushButton(Qt.QIcon(common.USER), '')
        user_button.setObjectName('Flat')
        user_button.setCursor(Qt.Qt.PointingHandCursor)
        user_button.setIconSize(Qt.QSize(40, 40))
        user_button.setFixedSize(Qt.QSize(60, 60))
        user_button.setMenu(user_menu)

        scroll_area = Qt.QScrollArea()
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.setSizeConstraint(Qt.QLayout.SetMinimumSize)

        for exam in list_of_exams:
            exam_id = exam['rowid']
            exam_name = exam['name']

            exam_button = Qt.QPushButton(Qt.QIcon(common.EXAM30), exam_name)
            exam_button.setObjectName('Flat')
            exam_button.setCursor(Qt.Qt.PointingHandCursor)
            exam_button.setIconSize(Qt.QSize(30, 30))
            exam_button.setFont(Qt.QFont('Arial', 20))
            exam_button.clicked.connect(common.return_lambda(app.display_exam, exam_id))

            exam_layout = Qt.QHBoxLayout()
            exam_layout.addWidget(exam_button)
            exam_layout.addStretch(1)

            scroll_layout.addLayout(exam_layout)

        scroll_layout.addStretch(1)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addStretch(1)
        upper_layout.addWidget(exams_title)
        upper_layout.addStretch(1)
        upper_layout.addWidget(user_button)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(scroll_area)
        self.setLayout(layout)
