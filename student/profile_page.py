"""
Page with user profile.
"""


from PyQt5 import Qt
import common


class ProfilePage(Qt.QWidget):
    """
    Page with user profile.
    """
    def __init__(self, app, group_name, user_name):
        super().__init__()

        back_button = Qt.QPushButton(Qt.QIcon(common.LEFT), '', self)
        back_button.setObjectName('Flat')
        back_button.setCursor(Qt.Qt.PointingHandCursor)
        back_button.setIconSize(Qt.QSize(35, 35))
        back_button.setFixedSize(Qt.QSize(55, 55))
        back_button.clicked.connect(lambda _: app.display_home_page())

        profile_title = Qt.QLabel('Профиль', self)
        profile_title.setFont(Qt.QFont('Arial', 30))
        profile_title.setAlignment(Qt.Qt.AlignCenter)

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        info_title = Qt.QLabel('Информация', self)
        info_title.setFont(Qt.QFont('Arial', 25))

        user_title = Qt.QLabel('Имя пользователя:', self)
        user_title.setFont(Qt.QFont('Arial', 20))

        user_label = Qt.QLabel(user_name, self)
        user_label.setFont(Qt.QFont('Arial', 20, 65, True))

        group_title = Qt.QLabel('Состоит в группе:', self)
        group_title.setFont(Qt.QFont('Arial', 20))

        group_label = Qt.QLabel(group_name, self)
        group_label.setFont(Qt.QFont('Arial', 20, 65, True))

        change_password_title = Qt.QLabel('Изменить пароль', self)
        change_password_title.setFont(Qt.QFont('Arial', 25))

        old_password_title = Qt.QLabel('Старый пароль:', self)
        old_password_title.setFont(Qt.QFont('Arial', 20))

        self.old_password_input = Qt.QLineEdit(self)
        self.old_password_input.setFont(Qt.QFont('Arial', 20))
        self.old_password_input.setMinimumWidth(400)
        self.old_password_input.setEchoMode(Qt.QLineEdit.Password)

        new_password_title = Qt.QLabel('Новый пароль:', self)
        new_password_title.setFont(Qt.QFont('Arial', 20))

        self.new_password_input = Qt.QLineEdit(self)
        self.new_password_input.setFont(Qt.QFont('Arial', 20))
        self.new_password_input.setMinimumWidth(400)
        self.new_password_input.setEchoMode(Qt.QLineEdit.Password)
        self.new_password_input.textChanged.connect(self.update_change_password_button_state)

        repeat_title = Qt.QLabel('Повторите пароль:', self)
        repeat_title.setFont(Qt.QFont('Arial', 20))

        self.repeat_input = Qt.QLineEdit(self)
        self.repeat_input.setFont(Qt.QFont('Arial', 20))
        self.repeat_input.setMinimumWidth(400)
        self.repeat_input.setEchoMode(Qt.QLineEdit.Password)
        self.repeat_input.textChanged.connect(self.update_change_password_button_state)

        self.change_password_button = Qt.QPushButton('Изменить пароль', self)
        self.change_password_button.setObjectName('Button')
        self.change_password_button.setFont(Qt.QFont('Arial', 20))
        self.change_password_button.clicked.connect(lambda: app.change_password(
            self.old_password_input.text(), self.new_password_input.text()))

        self.status_label = Qt.QLabel(self)
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.status_label.setWordWrap(True)

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addWidget(profile_title)

        info_title_layout = Qt.QVBoxLayout()
        info_title_layout.addWidget(user_title)
        info_title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        info_title_layout.addWidget(group_title)

        info_label_layout = Qt.QVBoxLayout()
        info_label_layout.addWidget(user_label)
        info_label_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        info_label_layout.addWidget(group_label)

        info_layout = Qt.QHBoxLayout()
        info_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        info_layout.addLayout(info_title_layout)
        info_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        info_layout.addLayout(info_label_layout)
        info_layout.addStretch(1)

        change_password_title_layout = Qt.QVBoxLayout()
        change_password_title_layout.addWidget(old_password_title)
        change_password_title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        change_password_title_layout.addWidget(new_password_title)
        change_password_title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        change_password_title_layout.addWidget(repeat_title)

        change_password_input_layout = Qt.QVBoxLayout()
        change_password_input_layout.addWidget(self.old_password_input)
        change_password_input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        change_password_input_layout.addWidget(self.new_password_input)
        change_password_input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        change_password_input_layout.addWidget(self.repeat_input)

        change_password_main_layout = Qt.QHBoxLayout()
        change_password_main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        change_password_main_layout.addLayout(change_password_title_layout)
        change_password_main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        change_password_main_layout.addLayout(change_password_input_layout)
        change_password_main_layout.addStretch(1)

        change_password_button_layout = Qt.QHBoxLayout()
        change_password_button_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        change_password_button_layout.addWidget(self.change_password_button)
        change_password_button_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        change_password_button_layout.addWidget(self.status_label)
        change_password_button_layout.addStretch(1)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        scroll_layout.addWidget(info_title)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        scroll_layout.addLayout(info_layout)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 30))
        scroll_layout.addWidget(change_password_title)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        scroll_layout.addLayout(change_password_main_layout)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        scroll_layout.addLayout(change_password_button_layout)
        scroll_layout.addStretch(1)

        scroll_widget = Qt.QWidget(self)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def update_change_password_button_state(self):
        """
        Determines the state of change_password_button.
        """
        if self.new_password_input.text() == self.repeat_input.text():
            self.change_password_button.setEnabled(True)
            self.repeat_input.setStyleSheet('border-color: ' + common.GREEN)
        else:
            self.change_password_button.setDisabled(True)
            self.repeat_input.setStyleSheet('border-color: ' + common.RED)

    def set_waiting_state(self):
        """
        Sets waiting state.
        """
        self.setCursor(Qt.Qt.WaitCursor)
        self.status_label.setText('Подождите...')
        self.status_label.setStyleSheet('color: black')
        self.status_label.repaint()

    def set_failed_state(self, status):
        """
        Sets failed state.
        """
        self.setCursor(Qt.Qt.ArrowCursor)
        self.status_label.setText(status)
        self.status_label.setStyleSheet('color: ' + common.RED)
