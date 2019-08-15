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

        info_title = Qt.QLabel('Информация', self)
        info_title.setFont(Qt.QFont('Arial', 25))


        change_password_title = Qt.QLabel('Изменить пароль', self)
        change_password_title.setFont(Qt.QFont('Arial', 25))

        old_password_title = Qt.QLabel('Старый пароль:', self)
        old_password_title.setFont(Qt.QFont('Arial', 20))

        old_password_input = Qt.QLineEdit(self)
        old_password_input.setFont(Qt.QFont('Arial', 20))
        old_password_input.setMinimumWidth(400)
        old_password_input.setEchoMode(Qt.QLineEdit.Password)

        new_password_title = Qt.QLabel('Новый пароль:', self)
        new_password_title.setFont(Qt.QFont('Arial', 20))

        new_password_input = Qt.QLineEdit(self)
        new_password_input.setFont(Qt.QFont('Arial', 20))
        new_password_input.setMinimumWidth(400)
        new_password_input.setEchoMode(Qt.QLineEdit.Password)

        repeat_title = Qt.QLabel('Повторите пароль:', self)
        repeat_title.setFont(Qt.QFont('Arial', 20))

        repeat_input = Qt.QLineEdit(self)
        repeat_input.setFont(Qt.QFont('Arial', 20))
        repeat_input.setMinimumWidth(400)
        repeat_input.setEchoMode(Qt.QLineEdit.Password)

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addWidget(profile_title)

        info_layout = Qt.QVBoxLayout()

        change_password_title_layout = Qt.QVBoxLayout()
        change_password_title_layout.addWidget(old_password_title)
        change_password_title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        change_password_title_layout.addWidget(new_password_title)
        change_password_title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        change_password_title_layout.addWidget(repeat_title)

        change_password_input_layout = Qt.QVBoxLayout()
        change_password_input_layout.addWidget(old_password_input)
        change_password_input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        change_password_input_layout.addWidget(new_password_input)
        change_password_input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        change_password_input_layout.addWidget(repeat_input)

        change_password_main_layout = Qt.QHBoxLayout()
        change_password_main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        change_password_main_layout.addLayout(change_password_title_layout)
        change_password_main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        change_password_main_layout.addLayout(change_password_input_layout)
        change_password_main_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        layout.addWidget(info_title)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(info_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 30))
        layout.addWidget(change_password_title)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(change_password_main_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        layout.addStretch(1)
        self.setLayout(layout)
