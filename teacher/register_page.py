"""
Register page for teacher.
"""


from PyQt5 import Qt
import common


class RegisterPage(Qt.QWidget):
    """
    Registration page for teacher.
    """
    def __init__(self, app):
        super().__init__()

        register_title = Qt.QLabel('Регистрация')
        register_title.setFont(Qt.QFont('Arial', 30))
        register_title.setAlignment(Qt.Qt.AlignCenter)

        group_title = Qt.QLabel('Название группы:')
        group_title.setFont(Qt.QFont('Arial', 20))

        group_input = Qt.QLineEdit()
        group_input.setFont(Qt.QFont('Arial', 20))
        group_input.setMinimumWidth(400)

        user_title = Qt.QLabel('Ваш логин:')
        user_title.setFont(Qt.QFont('Arial', 20))

        user_input = Qt.QLineEdit()
        user_input.setFont(Qt.QFont('Arial', 20))
        user_input.setMinimumWidth(400)

        password_title = Qt.QLabel('Придумайте пароль:')
        password_title.setFont(Qt.QFont('Arial', 20))

        self.password_input = Qt.QLineEdit()
        self.password_input.setFont(Qt.QFont('Arial', 20))
        self.password_input.setMinimumWidth(400)
        self.password_input.setEchoMode(Qt.QLineEdit.Password)
        self.password_input.textChanged.connect(self.update_button_state)

        repeat_title = Qt.QLabel('Повторите пароль:')
        repeat_title.setFont(Qt.QFont('Arial', 20))

        self.repeat_input = Qt.QLineEdit()
        self.repeat_input.setFont(Qt.QFont('Arial', 20))
        self.repeat_input.setMinimumWidth(400)
        self.repeat_input.setEchoMode(Qt.QLineEdit.Password)
        self.repeat_input.textChanged.connect(self.update_button_state)

        self.register_button = Qt.QPushButton('Зарегистрироваться')
        self.register_button.setObjectName('Button')
        self.register_button.setFont(Qt.QFont('Arial', 20))
        self.register_button.clicked.connect(lambda: app.register(
            group_input.text(), user_input.text(), self.password_input.text()))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.status_label.setMinimumWidth(380)

        settings_button = Qt.QPushButton(Qt.QIcon(common.SETTINGS), '')
        settings_button.setObjectName('Flat')
        settings_button.setCursor(Qt.Qt.PointingHandCursor)
        settings_button.setIconSize(Qt.QSize(40, 40))
        settings_button.clicked.connect(app.display_settings_page)

        enter_button = Qt.QPushButton('Вход')
        enter_button.setObjectName('Flat')
        enter_button.setCursor(Qt.Qt.PointingHandCursor)
        enter_button.setFont(Qt.QFont('Arial', 20))
        enter_button.clicked.connect(app.display_login_page)
        enter_button.setStyleSheet('color: ' + common.GREY)

        title_layout = Qt.QVBoxLayout()
        title_layout.addWidget(group_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(user_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(password_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(repeat_title)

        input_layout = Qt.QVBoxLayout()
        input_layout.addWidget(group_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(user_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(self.password_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(self.repeat_input)

        main_layout = Qt.QHBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)
        main_layout.addStretch(1)

        button_layout = Qt.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.register_button)
        button_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        button_layout.addWidget(self.status_label)
        button_layout.addStretch(1)

        lower_layout = Qt.QHBoxLayout()
        lower_layout.addWidget(settings_button)
        lower_layout.addStretch(1)
        lower_layout.addWidget(enter_button)

        layout = Qt.QVBoxLayout()
        layout.addWidget(register_title)
        layout.addStretch(1)
        layout.addLayout(main_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 60))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        layout.addLayout(lower_layout)
        self.setLayout(layout)

    def update_button_state(self):
        """
        Determines the state of register button.
        """
        if self.password_input.text() == self.repeat_input.text():
            self.register_button.setEnabled(True)
            self.repeat_input.setStyleSheet('border-color: ' + common.GREEN)
        else:
            self.register_button.setDisabled(True)
            self.repeat_input.setStyleSheet('border-color: ' + common.RED)

    def set_waiting_state(self):
        """
        Sets waiting state.
        """
        self.setCursor(Qt.Qt.WaitCursor)
        self.status_label.setText('Подождите...')
        self.status_label.setStyleSheet('color: black')
        self.status_label.repaint()

    def set_failed_state(self):
        """
        Sets failed state.
        """
        self.setCursor(Qt.Qt.ArrowCursor)
        self.status_label.setText('Попробуйте ещё раз')
        self.status_label.setStyleSheet('color: ' + common.RED)
