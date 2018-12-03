"""
Safe connection to server.
"""


import os
import socket
from xmlrpc.client import ServerProxy


class User:
    """
    Safe connection to server.
    """
    def __init__(self, application):
        self.application = application
        self.server = None
        self.group = ''
        self.user = ''
        self.password = ''

    def update_user_info(self, group, user, password):
        """
        Updates client's data: group, user, password.
        """
        self.group = group
        self.user = user
        self.password = password

    @staticmethod
    def read_ip():
        """
        Returns current ip-address of server.
        """
        return open(os.path.join('client', 'server.txt'), encoding='utf-8-sig').read()

    def update_ip(self, ip_address):
        """
        Updates current ip-address of server.
        """
        open(os.path.join('client', 'server.txt'), 'w', encoding='utf-8-sig').write(ip_address)
        self.server = ServerProxy('http://' + ip_address + ':8000')

    def login(self):
        """
        Tries to login the student.
        """
        return self.server.login(self.group, self.user, self.password)

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
