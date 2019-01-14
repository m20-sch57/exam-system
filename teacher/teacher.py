"""
Examiner project, teacher module.
"""


import sys
import os
import socket
import functools

from user import User
from PyQt5 import Qt
from settings_page import SettingsPage
from login_page import LoginPage
from register_page import RegisterPage
from register_success_page import RegisterSuccessPage


def safe(function):
    """
    Returns safe function.
    """
    @functools.wraps(function)
    def result(self, *args, **kwargs):
        try:
            return function(self, *args, **kwargs)
        except socket.error:
            self.display_settings_page()
            self.widget.set_failed_state()
    return result


class Application(Qt.QApplication):
    """
    Main application class.
    """
    def __init__(self):
        super().__init__(sys.argv)
        self.user = User()
        self.window = Qt.QWidget()
        self.window.setStyleSheet(open(os.path.join('css', 'common_style.css')).read())
        self.window.setWindowTitle('Учитель')
        self.window.setGeometry(200, 100, 1000, 700)
        self.widget = Qt.QWidget(self.window)
        self.layout = Qt.QHBoxLayout(self.window)
        self.layout.addWidget(self.widget)
        self.window.show()

    def display_widget(self, widget):
        """
        Displays the widget.
        """
        old = self.widget
        old.deleteLater()
        self.layout.removeWidget(old)
        self.layout.addWidget(widget)
        self.widget = widget

    def start(self):
        """
        Starts application.
        """
        self.display_login_page()
        self.exit(self.exec_())

    def check_ip(self, ip_address):
        """
        Checks ip-address of server.
        """
        try:
            self.widget.set_waiting_state()
            self.user.set_item('server', ip_address)
            self.user.update_server()
            self.user.ping()
            self.widget.set_succeeded_state()
        except socket.error:
            self.widget.set_failed_state()

    @safe
    def save_settings(self, settings):
        """
        Saves all settings.
        """
        for item in settings.keys():
            self.user.set_item(item, str(settings[item]))
        self.display_login_page()

    def display_settings_page(self):
        """
        Displays server error page.
        """
        self.display_widget(SettingsPage(
            self.user.get_settings(), self.check_ip, self.display_login_page, self.save_settings))

    def display_login_page(self):
        """
        Displays login page for teacher.
        """
        self.display_widget(LoginPage(
            self.user, self.login, self.display_register_page, self.display_settings_page))

    def display_register_page(self):
        """
        Displays register page for teacher.
        """
        self.display_widget(RegisterPage(
            self.register, self.display_login_page, self.display_settings_page))

    def display_register_success_page(self):
        """
        Displays success registration page.
        """
        self.display_widget(RegisterSuccessPage(
            self.display_register_page, self.display_login_page))

    @safe
    def register(self, group, user, password):
        """
        Tries to register the teacher.
        """
        self.widget.set_waiting_state()
        self.user.update_user_info(group, user, password)
        success = self.user.register()
        if not success:
            self.widget.set_failed_state()
        else:
            self.display_register_success_page()

    @safe
    def login(self, group, user, password):
        """
        Tries to login the teacher.
        """
        self.widget.set_waiting_state()
        self.user.update_user_info(group, user, password)
        success = self.user.login()
        if not success:
            self.widget.set_failed_state()
        else:
            self.display_home_page()

    @safe
    def logout(self):
        """
        Logs out the teacher.
        """
        self.display_login_page()


if __name__ == "__main__":
    APP = Application()
    APP.start()
