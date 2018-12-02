"""
Login page for student.
"""


from PyQt5.Qt import Qt, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.Qt import QLabel, QLineEdit, QPushButton
from PyQt5.Qt import QFont, QSize, QSpacerItem


class LoginPage(QWidget):
    """
    Login page for student.
    """
    def __init__(self, user, current_ip, status, login_function):
        super().__init__()

        enter_title = QLabel('Вход в систему')
        enter_title.setFont(QFont('Arial', 30))
        enter_title.setAlignment(Qt.AlignCenter)

        group_title = QLabel('Группа:')
        group_title.setFont(QFont('Arial', 20))

        group_input = QLineEdit(user.group)
        group_input.setFont(QFont('Arial', 20))
        group_input.setMinimumWidth(400)
        group_input.setText('M20 История') # TODO: REMOVE THEN!

        user_title = QLabel('Логин:')
        user_title.setFont(QFont('Arial', 20))

        user_input = QLineEdit(user.user)
        user_input.setFont(QFont('Arial', 20))
        user_input.setMinimumWidth(400)
        user_input.setText('Фёдор Куянов') # TODO: REMOVE THEN!

        password_title = QLabel('Пароль:')
        password_title.setFont(QFont('Arial', 20))

        password_input = QLineEdit(user.password)
        password_input.setFont(QFont('Arial', 20))
        password_input.setMinimumWidth(400)
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setText('12345') # TODO: REMOVE THEN!

        enter_button = QPushButton('Войти в систему')
        enter_button.setFont(QFont('Arial', 20))
        enter_button.setMinimumSize(QSize(250, 50))
        enter_button.clicked.connect(lambda: login_function(
            group_input.text(), user_input.text(), password_input.text(), server_input.text()))

        self.status_label = QLabel(status)
        self.status_label.setFont(QFont('Arial', 20))
        self.status_label.setMinimumWidth(270)
        self.status_label.setStyleSheet('color: red')

        server_title = QLabel('IP-адрес сервера:')
        server_title.setFont(QFont('Arial', 15))

        server_input = QLineEdit(current_ip)
        server_input.setFont(QFont('Arial', 15))
        server_input.setMinimumWidth(300)
        server_input.setStyleSheet('background: #F0F0F0')

        title_layout = QVBoxLayout()
        title_layout.addWidget(group_title)
        title_layout.addSpacerItem(QSpacerItem(0, 20))
        title_layout.addWidget(user_title)
        title_layout.addSpacerItem(QSpacerItem(0, 20))
        title_layout.addWidget(password_title)

        input_layout = QVBoxLayout()
        input_layout.addWidget(group_input)
        input_layout.addSpacerItem(QSpacerItem(0, 20))
        input_layout.addWidget(user_input)
        input_layout.addSpacerItem(QSpacerItem(0, 20))
        input_layout.addWidget(password_input)

        main_layout = QHBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)
        main_layout.addStretch(1)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(enter_button)
        button_layout.addSpacerItem(QSpacerItem(20, 0))
        button_layout.addWidget(self.status_label)
        button_layout.addStretch(1)

        server_layout = QHBoxLayout()
        server_layout.addStretch(1)
        server_layout.addWidget(server_title)
        server_layout.addSpacerItem(QSpacerItem(20, 0))
        server_layout.addWidget(server_input)
        server_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addWidget(enter_title)
        layout.addStretch(1)
        layout.addLayout(main_layout)
        layout.addSpacerItem(QSpacerItem(0, 60))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        layout.addLayout(server_layout)
        self.setLayout(layout)

    def set_waiting_state(self):
        """
        Sets state to waiting.
        """
        self.setCursor(Qt.WaitCursor)
        self.status_label.setText('Подождите...')
        self.status_label.setStyleSheet('color: black')
        self.status_label.repaint()
