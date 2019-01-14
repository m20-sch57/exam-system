"""
Login page for student.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class LoginPage(Qt.QWidget):
    """
    Login page for student.
    """
    def __init__(self, user, login_function, register_function, settings_function):
        super().__init__()

        enter_title = Qt.QLabel('Вход в систему')
        enter_title.setFont(Qt.QFont('Arial', 30))
        enter_title.setAlignment(Qt.Qt.AlignCenter)

        group_title = Qt.QLabel('Группа:')
        group_title.setFont(Qt.QFont('Arial', 20))

        group_input = Qt.QLineEdit(user.group)
        group_input.setFont(Qt.QFont('Arial', 20))
        group_input.setMinimumWidth(400)

        user_title = Qt.QLabel('Логин:')
        user_title.setFont(Qt.QFont('Arial', 20))

        user_input = Qt.QLineEdit(user.user)
        user_input.setFont(Qt.QFont('Arial', 20))
        user_input.setMinimumWidth(400)

        password_title = Qt.QLabel('Пароль:')
        password_title.setFont(Qt.QFont('Arial', 20))

        password_input = Qt.QLineEdit()
        password_input.setFont(Qt.QFont('Arial', 20))
        password_input.setMinimumWidth(400)
        password_input.setEchoMode(Qt.QLineEdit.Password)
        if user.get_item('autofill') == 'True':
            password_input.setText(user.password)

        enter_button = Qt.QPushButton('Войти в систему')
        enter_button.setFont(Qt.QFont('Arial', 20))
        enter_button.clicked.connect(lambda: login_function(
            group_input.text(), user_input.text(), password_input.text()))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.status_label.setMinimumWidth(270)

        settings_button = FlatButton(Qt.QIcon(common.SETTINGS), '')
        settings_button.setIconSize(Qt.QSize(40, 40))
        settings_button.clicked.connect(lambda _: settings_function())

        register_button = FlatButton('Регистрация')
        register_button.setFont(Qt.QFont('Arial', 20))
        register_button.clicked.connect(lambda _: register_function())
        register_button.setStyleSheet('color: ' + common.GREY)

        title_layout = Qt.QVBoxLayout()
        title_layout.addWidget(group_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(user_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(password_title)

        input_layout = Qt.QVBoxLayout()
        input_layout.addWidget(group_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
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
