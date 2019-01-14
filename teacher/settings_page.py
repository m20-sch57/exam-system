"""
Settings page.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class SettingsPage(Qt.QWidget):
    """
    Settings page.
    """
    def __init__(self, settings, check_ip_function, back_function, save_function):
        super().__init__()

        back_button = FlatButton(Qt.QIcon(common.LEFT), '')
        back_button.setIconSize(Qt.QSize(40, 40))
        back_button.clicked.connect(lambda _: back_function())

        settings_title = Qt.QLabel('Настройки')
        settings_title.setFont(Qt.QFont('Arial', 30))
        settings_title.setAlignment(Qt.Qt.AlignCenter)

        server_title = Qt.QLabel('Соединение с сервером')
        server_title.setFont(Qt.QFont('Arial', 25))

        server_ip_title = Qt.QLabel('IP-адрес сервера:')
        server_ip_title.setFont(Qt.QFont('Arial', 20))

        server_ip_input = Qt.QLineEdit(settings['server'])
        server_ip_input.setMinimumWidth(350)

        server_check_button = Qt.QPushButton('Проверить соединение')
        server_check_button.clicked.connect(lambda: check_ip_function(server_ip_input.text()))

        self.server_status_label = Qt.QLabel()
        self.server_status_label.setFont(Qt.QFont('Arial', 20))
        self.server_status_label.setMinimumWidth(270)

        autosave_title = Qt.QLabel('Автозаполнение форм')
        autosave_title.setFont(Qt.QFont('Arial', 25))

        autosave_password_checkbox = Qt.QCheckBox('Сохранять пароль')
        autosave_password_checkbox.setFont(Qt.QFont('Arial', 20))
        if settings['autofill'] == 'True':
            autosave_password_checkbox.setChecked(True)

        save_button = Qt.QPushButton('Сохранить')
        save_button.clicked.connect(lambda: save_function(
            {'server': server_ip_input.text(),
             'autofill': autosave_password_checkbox.isChecked()
            }
        ))

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addStretch(1)
        upper_layout.addWidget(settings_title)
        upper_layout.addStretch(1)

        server_ip_layout = Qt.QHBoxLayout()
        server_ip_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        server_ip_layout.addWidget(server_ip_title)
        server_ip_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        server_ip_layout.addWidget(server_ip_input)
        server_ip_layout.addStretch(1)

        server_check_layout = Qt.QHBoxLayout()
        server_check_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        server_check_layout.addWidget(server_check_button)
        server_check_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        server_check_layout.addWidget(self.server_status_label)
        server_check_layout.addStretch(1)

        server_layout = Qt.QVBoxLayout()
        server_layout.addLayout(server_ip_layout)
        server_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        server_layout.addLayout(server_check_layout)

        autosave_password_layout = Qt.QHBoxLayout()
        autosave_password_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        autosave_password_layout.addWidget(autosave_password_checkbox)
        autosave_password_layout.addStretch(1)

        autosave_layout = Qt.QVBoxLayout()
        autosave_layout.addLayout(autosave_password_layout)

        save_layout = Qt.QHBoxLayout()
        save_layout.addWidget(save_button)
        save_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        layout.addWidget(server_title)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(server_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 30))
        layout.addWidget(autosave_title)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(autosave_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        layout.addStretch(1)
        layout.addLayout(save_layout)
        self.setLayout(layout)

    def set_waiting_state(self):
        """
        Sets waiting state.
        """
        self.setCursor(Qt.Qt.WaitCursor)
        self.server_status_label.setText('Подождите...')
        self.server_status_label.setStyleSheet('color: black')
        self.server_status_label.repaint()

    def set_failed_state(self):
        """
        Sets failed state.
        """
        self.setCursor(Qt.Qt.ArrowCursor)
        self.server_status_label.setText('Сервер не отвечает')
        self.server_status_label.setStyleSheet('color: ' + common.RED)

    def set_succeeded_state(self):
        """
        Sets succeeded state.
        """
        self.setCursor(Qt.Qt.ArrowCursor)
        self.server_status_label.setText('Всё в порядке')
        self.server_status_label.setStyleSheet('color: ' + common.GREEN)
