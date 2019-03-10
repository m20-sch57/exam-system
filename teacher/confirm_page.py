"""
Page that asks to confirm the action.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class ConfirmPage(Qt.QWidget):
    """
    Page that asks to confirm the action.
    """
    def __init__(self, text, back_function, main_function):
        super().__init__()

        back_button = FlatButton(Qt.QIcon(common.LEFT), '')
        back_button.setIconSize(Qt.QSize(40, 40))
        back_button.clicked.connect(lambda _: back_function())

        confirm_title = Qt.QLabel('Подтвердите действие')
        confirm_title.setFont(Qt.QFont('Arial', 30))

        confirm_label = Qt.QLabel(text)
        confirm_label.setFont(Qt.QFont('Arial', 25))
        confirm_label.setAlignment(Qt.Qt.AlignCenter)
        confirm_label.setWordWrap(True)
        confirm_label.setStyleSheet('color: red')

        yes_button = Qt.QPushButton(Qt.QIcon(common.TICK), 'Да, продолжить')
        yes_button.setIconSize(Qt.QSize(40, 40))
        yes_button.setFont(Qt.QFont('Arial', 20))
        yes_button.clicked.connect(lambda _: main_function())

        no_button = Qt.QPushButton(Qt.QIcon(common.CROSS), 'Нет, отменить')
        no_button.setIconSize(Qt.QSize(40, 40))
        no_button.setFont(Qt.QFont('Arial', 20))
        no_button.clicked.connect(lambda _: back_function())

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addStretch(1)
        upper_layout.addWidget(confirm_title)
        upper_layout.addStretch(1)

        button_layout = Qt.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(yes_button)
        button_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        button_layout.addWidget(no_button)
        button_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addStretch(1)
        layout.addWidget(confirm_label)
        layout.addSpacerItem(Qt.QSpacerItem(0, 30))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)
