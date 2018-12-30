"""
Page with settings: current ip-address of server.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class SettingsPage(Qt.QWidget):
    """
    Settings page.
    """
    def __init__(self, current_ip, save_function, back_function):
        super().__init__()

        back_button = FlatButton(Qt.QIcon(common.LEFT), '')
        back_button.setIconSize(Qt.QSize(40, 40))
        back_button.clicked.connect(lambda arg: back_function())

        settings_title = Qt.QLabel('Настройки')
        settings_title.setFont(Qt.QFont('Arial', 30))
        settings_title.setAlignment(Qt.Qt.AlignCenter)

        server_title = Qt.QLabel('IP-адрес сервера:')
        server_title.setFont(Qt.QFont('Arial', 20))
        server_title.setAlignment(Qt.Qt.AlignCenter)
        server_title.setMinimumWidth(250)

        server_input = Qt.QLineEdit(current_ip)
        server_input.setMinimumWidth(400)

        check_button = Qt.QPushButton('Обновить IP-адрес')
        check_button.clicked.connect(lambda: save_function(server_input.text()))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.status_label.setMinimumWidth(270)

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addStretch(1)
        upper_layout.addWidget(settings_title)
        upper_layout.addStretch(1)

        server_upper_layout = Qt.QHBoxLayout()
        server_upper_layout.addWidget(server_title)
        server_upper_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        server_upper_layout.addWidget(server_input)
        server_upper_layout.addStretch(1)

        server_lower_layout = Qt.QHBoxLayout()
        server_lower_layout.addWidget(check_button)
        server_lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        server_lower_layout.addWidget(self.status_label)
        server_lower_layout.addStretch(1)

        server_layout = Qt.QVBoxLayout()
        server_layout.addLayout(server_upper_layout)
        server_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        server_layout.addLayout(server_lower_layout)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 30))
        layout.addLayout(server_layout)
        layout.addStretch(1)
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
        self.status_label.setText('Сервер не отвечает')
        self.status_label.setStyleSheet('color: ' + common.RED)

    def set_succeeded_state(self):
        """
        Sets succeeded state.
        """
        self.setCursor(Qt.Qt.ArrowCursor)
        self.status_label.setText('Всё в порядке')
        self.status_label.setStyleSheet('color: ' + common.GREEN)
