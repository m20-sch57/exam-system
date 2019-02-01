"""
Safe connection to server.
"""


import os
import socket
import hashlib
from xmlrpc.client import ServerProxy


class User:
    """
    Safe connection to server.
    """
    def __init__(self):
        self.path = os.path.join('client')
        self.update_server()
        self.group = 'm20'
        self.user = 'Сергей Леонидович'
        self.password = '12345'

    def get_item(self, item):
        """
        Returns value of the item.
        """
        return open(os.path.join(self.path, item), encoding='utf-8-sig').read()

    def set_item(self, item, value):
        """
        Sets value of the item.
        """
        open(os.path.join(self.path, item), 'w', encoding='utf-8-sig').write(value)

    def get_settings(self):
        """
        Returns map of all settings.
        """
        settings = {}
        for item in os.listdir(self.path):
            settings[item] = self.get_item(item)
        return settings

    def update_user_info(self, group, user, password):
        """
        Updates client's info: group, user, password.
        """
        self.group = group
        self.user = user
        self.password = password

    def update_server(self):
        """
        Updates self.server.
        """
        self.server = ServerProxy('http://' + self.get_item('server'))

    def ping(self):
        """
        Checks if server is available.
        """
        self.server.ping()

    def register(self):
        """
        Tries to register the teacher.
        """
        password_hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
        return self.server.register_teacher(self.group, self.user, password_hash)

    def login(self):
        """
        Tries to login the teacher.
        """
        password_hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
        return self.server.login_teacher(self.group, self.user, password_hash)

    def list_of_exams(self):
        """
        Returns list of all available exams.
        """
        return self.server.list_of_exams(self.group)

    def get_exam(self, exam):
        """
        Returns all question data in the exam.
        """
        return self.server.get_exam_data(self.group, exam)

    def get_exam_info(self, exam):
        """
        Returns exam's info.
        """
        return self.server.get_exam_info(self.group, exam)


socket.setdefaulttimeout(3)
