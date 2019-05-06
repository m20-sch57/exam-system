"""
Teacher's home page.
"""


from PyQt5 import Qt
import common


class HomePage(Qt.QWidget):
    """
    Teacher's home page.
    """
    def __init__(self, app):
        super().__init__()
        list_of_exams = app.list_of_exams()

        exams_title = Qt.QLabel('Доступные экзамены', self)
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

        user_button = Qt.QPushButton(Qt.QIcon(common.USER), '', self)
        user_button.setObjectName('Flat')
        user_button.setCursor(Qt.Qt.PointingHandCursor)
        user_button.setIconSize(Qt.QSize(35, 35))
        user_button.setFixedSize(Qt.QSize(55, 55))
        user_button.setMenu(user_menu)

        scroll_area = Qt.QScrollArea()
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.setSizeConstraint(Qt.QLayout.SetMinimumSize)

        for exam in list_of_exams:
            exam_id = exam['rowid']
            exam_name = exam['name']

            exam_button = Qt.QPushButton(Qt.QIcon(common.EXAM30), exam_name, self)
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

        scroll_widget = Qt.QWidget(self)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        create_button = Qt.QPushButton(Qt.QIcon(common.CREATE), 'Создать экзамен', self)
        create_button.setObjectName('Button')
        create_button.setIconSize(Qt.QSize(35, 35))
        create_button.setFont(Qt.QFont('Arial', 20))
        create_button.clicked.connect(lambda _: app.create_exam())

        info_label = Qt.QLabel('Всего экзаменов - ' + str(len(list_of_exams)), self)
        info_label.setFont(Qt.QFont('Arial', 20))

        lower_layout = Qt.QHBoxLayout()
        lower_layout.addWidget(create_button)
        lower_layout.addStretch(1)
        lower_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        lower_layout.addWidget(info_label)
        lower_layout.addSpacerItem(Qt.QSpacerItem(10, 0))

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addStretch(1)
        upper_layout.addWidget(exams_title)
        upper_layout.addStretch(1)
        upper_layout.addWidget(user_button)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(scroll_area)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(lower_layout)
        self.setLayout(layout)
