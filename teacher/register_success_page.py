"""
Page that is displayed after teacher has successfully registered.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class RegisterSuccessPage(Qt.QWidget):
    """
    Successful registration page.
    """
    def __init__(self, back_function, enter_function):
        super().__init__()

        back_button = FlatButton(Qt.QIcon(common.LEFT), '')
        back_button.setIconSize(Qt.QSize(40, 40))
        back_button.clicked.connect(lambda _: back_function())

        register_title = Qt.QLabel('Регистрация')
        register_title.setFont(Qt.QFont('Arial', 30))
        register_title.setAlignment(Qt.Qt.AlignCenter)

        status_img = Qt.QLabel()
        status_img.setScaledContents(True)
        status_img.setPixmap(Qt.QPixmap(common.TICK))
        status_img.setFixedSize(Qt.QSize(50, 50))

        status_label = Qt.QLabel('Вы успешно зарегистрированы!')
        status_label.setFont(Qt.QFont('Arial', 25))
        status_label.setStyleSheet('color: ' + common.GREEN)

        enter_button = Qt.QPushButton('Продолжить')
        enter_button.setFont(Qt.QFont('Arial', 20))
        enter_button.clicked.connect(lambda _: enter_function())

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addStretch(1)
        upper_layout.addWidget(register_title)
        upper_layout.addStretch(1)

        status_layout = Qt.QHBoxLayout()
        status_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        status_layout.addWidget(status_img)
        status_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        status_layout.addWidget(status_label)
        status_layout.addStretch(1)

        enter_layout = Qt.QHBoxLayout()
        enter_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        enter_layout.addWidget(enter_button)
        enter_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 30))
        layout.addLayout(status_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(enter_layout)
        layout.addStretch(1)
        self.setLayout(layout)
