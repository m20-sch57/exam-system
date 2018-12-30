"""
Register page for student.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class RegisterPage(Qt.QWidget):
    """
    Registration page for student.
    """
    def __init__(self, user, register_function, login_function, settings_function):
        super().__init__()

        register_title = Qt.QLabel('Регистрация')
        register_title.setFont(Qt.QFont('Arial', 30))
        register_title.setAlignment(Qt.Qt.AlignCenter)

        group_title = Qt.QLabel('Название группы:')
        group_title.setFont(Qt.QFont('Arial', 20))

        group_input = Qt.QLineEdit(user.group)
        group_input.setMinimumWidth(400)
        group_input.textChanged.connect(lambda: user.update_user_info(
            group_input.text(), user_input.text(), password_input.text()))

        user_title = Qt.QLabel('Ваш логин:')
        user_title.setFont(Qt.QFont('Arial', 20))

        user_input = Qt.QLineEdit(user.user)
        user_input.setMinimumWidth(400)
        user_input.textChanged.connect(lambda: user.update_user_info(
            group_input.text(), user_input.text(), password_input.text()))

        password_title = Qt.QLabel('Придумайте пароль:')
        password_title.setFont(Qt.QFont('Arial', 20))

        password_input = Qt.QLineEdit(user.password)
        password_input.setMinimumWidth(400)
        password_input.setEchoMode(Qt.QLineEdit.Password)
        password_input.textChanged.connect(lambda: user.update_user_info(
            group_input.text(), user_input.text(), password_input.text()))

        repeat_title = Qt.QLabel('Повторите пароль:')
        repeat_title.setFont(Qt.QFont('Arial', 20))

        repeat_input = Qt.QLineEdit()
        repeat_input.setMinimumWidth(400)
        repeat_input.setEchoMode(Qt.QLineEdit.Password)

        register_button = Qt.QPushButton('Зарегистрироваться')
        register_button.clicked.connect(lambda arg: register_function())

        self.status_label = Qt.QLabel('')
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.status_label.setMinimumWidth(380)

        settings_button = FlatButton(Qt.QIcon(common.SETTINGS), '')
        settings_button.setIconSize(Qt.QSize(40, 40))
        settings_button.clicked.connect(lambda arg: settings_function())

        enter_button = FlatButton('Вход')
        enter_button.clicked.connect(lambda arg: login_function())
        enter_button.setStyleSheet('color: #546A74')

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
        input_layout.addWidget(password_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(repeat_input)

        main_layout = Qt.QHBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)
        main_layout.addStretch(1)

        button_layout = Qt.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(register_button)
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
