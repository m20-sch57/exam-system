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
        self.user = 'Фёдор Куянов'
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
        Tries to register the student.
        """
        password_hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
        return self.server.register(self.group, self.user, password_hash)

    def login(self):
        """
        Tries to login the student.
        """
        password_hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
        return self.server.login(self.group, self.user, password_hash)

    def list_of_exams(self):
        """
        Returns list of all available exams.
        """
        return self.server.list_of_exams(self.group)

    def get_exam(self, exam):
        """
        Returns all question data in the exam.
        """
        return self.server.get_exam(self.group, self.user, exam)

    def get_exam_info(self, exam):
        """
        Returns exam's info.
        """
        return self.server.get_exam_info(self.group, self.user, exam)

    def start_exam(self, exam):
        """
        Starts the exam.
        """
        return self.server.start_exam(self.group, self.user, exam)

    def finish_exam(self, exam):
        """
        Finishes the exam.
        """
        return self.server.finish_exam(self.group, self.user, exam)

    def save_answer(self, exam, question, answer):
        """
        Saves student's answer.
        """
        return self.server.save_answer(self.group, self.user, exam, question, answer)

    def check(self, exam, question):
        """
        Checks student's answer.
        """
        return self.server.check(self.group, self.user, exam, question)


socket.setdefaulttimeout(3)
