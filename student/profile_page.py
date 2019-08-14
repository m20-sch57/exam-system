"""
Page with user profile.
"""


from PyQt5 import Qt
import common


class ProfilePage(Qt.QWidget):
    """
    Page with user profile.
    """
    def __init__(self, app):
        super().__init__()

        back_button = Qt.QPushButton(Qt.QIcon(common.LEFT), '', self)
        back_button.setObjectName('Flat')
        back_button.setCursor(Qt.Qt.PointingHandCursor)
        back_button.setIconSize(Qt.QSize(35, 35))
        back_button.setFixedSize(Qt.QSize(55, 55))
        back_button.clicked.connect(app.display_home_page)

        profile_title = Qt.QLabel('Профиль', self)
        profile_title.setFont(Qt.QFont('Arial', 30))
        profile_title.setAlignment(Qt.Qt.AlignCenter)

        info_title = Qt.QLabel('Информация', self)
        info_title.setFont(Qt.QFont('Arial', 25))


        change_password_title = Qt.QLabel('Изменить пароль', self)
        change_password_title.setFont(Qt.QFont('Arial', 25))


        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addWidget(profile_title)

        info_layout = Qt.QVBoxLayout()

        change_password_layout = Qt.QVBoxLayout()

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        layout.addWidget(info_title)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(info_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 30))
        layout.addWidget(change_password_title)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(change_password_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        layout.addStretch(1)
        self.setLayout(layout)
