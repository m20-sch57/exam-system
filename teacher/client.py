"""
Contains client settings and server.
"""


import os
import socket
from xmlrpc.client import ServerProxy


class Client:
    """
    Contains client settings and server.
    """
    def __init__(self):
        self.path = os.path.join('client')
        self.user = False
        self.user_name = 'Админ'
        self.password = '12345'
        self.update_server()

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

    def update_server(self):
        """
        Updates self.server.
        """
        self.server = ServerProxy('http://' + self.get_item('server'))

    # def register(self):
    #     """
    #     Tries to register the teacher.
    #     """
    #     password_hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
    #     return self.server.register_teacher(self.group, self.user, password_hash)

    # def login(self):
    #     """
    #     Tries to login the teacher.
    #     """
    #     password_hash = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
    #     return self.server.login_teacher(self.group, self.user, password_hash)

    # def list_of_exams(self):
    #     """
    #     Returns list of all available exams.
    #     """
    #     return self.server.list_of_exams(self.group)

    # def get_exam(self, exam):
    #     """
    #     Returns all question data in the exam.
    #     """
    #     return self.server.get_exam_data(self.group, exam)

    # def get_exam_info(self, exam):
    #     """
    #     Returns exam's info.
    #     """
    #     return self.server.get_exam_info(self.group, exam)

    # def save_exam_settings(self, exam, settings):
    #     """
    #     Saves exam's settings.
    #     """
    #     return self.server.set_exam_info(self.group, exam, settings)

    # def save_question(self, exam, question, data):
    #     """
    #     Saves question data.
    #     """
    #     return self.server.set_question_data(self.group, exam, question, data)

    # def create_question(self, exam):
    #     """
    #     Creates question with this type.
    #     """
    #     return self.server.create_question(self.group, exam)

    # def reset_question(self, exam, question, question_type):
    #     """
    #     Assigns type of question to question_type.
    #     """
    #     return self.server.reset_question(self.group, exam, question, question_type)


socket.setdefaulttimeout(3)
