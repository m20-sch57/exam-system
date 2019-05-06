"""
Login page for student.
"""


from PyQt5 import Qt
import common


class LoginPage(Qt.QWidget):
    """
    Login page for student.
    """
    def __init__(self, app):
        super().__init__()

        enter_title = Qt.QLabel('Вход в систему', self)
        enter_title.setFont(Qt.QFont('Arial', 30))
        enter_title.setAlignment(Qt.Qt.AlignCenter)

        user_title = Qt.QLabel('Логин:', self)
        user_title.setFont(Qt.QFont('Arial', 20))

        user_input = Qt.QLineEdit(app.client.user_name, self)
        user_input.setFont(Qt.QFont('Arial', 20))
        user_input.setMinimumWidth(400)

        password_title = Qt.QLabel('Пароль:', self)
        password_title.setFont(Qt.QFont('Arial', 20))

        password_input = Qt.QLineEdit(self)
        password_input.setFont(Qt.QFont('Arial', 20))
        password_input.setMinimumWidth(400)
        password_input.setEchoMode(Qt.QLineEdit.Password)
        if app.client.get_data()['autofill']:
            password_input.setText(app.client.password)

        enter_button = Qt.QPushButton('Войти в систему', self)
        enter_button.setObjectName('Button')
        enter_button.setFont(Qt.QFont('Arial', 20))
        enter_button.clicked.connect(lambda: app.login(user_input.text(), password_input.text()))
        password_input.returnPressed.connect(enter_button.click)
        user_input.returnPressed.connect(enter_button.click)

        self.status_label = Qt.QLabel(self)
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.status_label.setMinimumWidth(270)

        settings_button = Qt.QPushButton(Qt.QIcon(common.SETTINGS), '', self)
        settings_button.setObjectName('Flat')
        settings_button.setCursor(Qt.Qt.PointingHandCursor)
        settings_button.setIconSize(Qt.QSize(35, 35))
        settings_button.setFixedSize(Qt.QSize(55, 55))
        settings_button.clicked.connect(app.display_settings_page)

        register_button = Qt.QPushButton('Регистрация', self)
        register_button.setObjectName('Flat')
        register_button.setCursor(Qt.Qt.PointingHandCursor)
        register_button.setFont(Qt.QFont('Arial', 20))
        register_button.clicked.connect(app.display_register_page)
        register_button.setStyleSheet('color: ' + common.GREY)

        title_layout = Qt.QVBoxLayout()
        title_layout.addWidget(user_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(password_title)

        input_layout = Qt.QVBoxLayout()
        input_layout.addWidget(user_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(password_input)

        main_layout = Qt.QHBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)
        main_layout.addStretch(1)

        button_layout = Qt.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(enter_button)
        button_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        button_layout.addWidget(self.status_label)
        button_layout.addStretch(1)

        lower_layout = Qt.QHBoxLayout()
        lower_layout.addWidget(settings_button)
        lower_layout.addStretch(1)
        lower_layout.addWidget(register_button)

        layout = Qt.QVBoxLayout()
        layout.addWidget(enter_title)
        layout.addStretch(1)
        layout.addLayout(main_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 60))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        layout.addLayout(lower_layout)
        self.setLayout(layout)

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
