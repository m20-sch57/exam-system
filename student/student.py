"""
Examiner project, student module.
"""


import sys
import socket
import functools
import hashlib

from user import User
from PyQt5 import Qt
from login_page import LoginPage
from home_page import HomePage
from start_exam_page import StartExamPage
from exam_page import ExamPage
from exam_status import ExamRunning, ExamFinished
from question_short import QuestionShort, QuestionShortChecked, QuestionShortDetails
from question_long import QuestionLong, QuestionLongDetails


def safe(function):
    """
    Returns safe function.
    """
    @functools.wraps(function)
    def result(self, *args, **kwargs):
        try:
            return function(self, *args, **kwargs)
        except socket.error:
            self.display_login_page('Сервер не отвечает')
    return result


class Application(Qt.QApplication):
    """
    Main application class.
    """
    def __init__(self):
        super().__init__(sys.argv)
        self.user = User(self)
        self.window = Qt.QWidget()
        self.window.setWindowTitle('Школьник')
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
        self.display_login_page('')
        self.exit(self.exec_())

    @safe
    def display_login_page(self, status):
        """
        Displays login page for student.
        """
        self.display_widget(LoginPage(self.user, self.user.read_ip(), status, self.login))

    @safe
    def display_home_page(self):
        """
        Displays home page with list of exams.
        """
        list_of_exams = self.user.list_of_exams()
        self.display_widget(HomePage(self.user, list_of_exams, self.display_exam))

    @safe
    def display_start_exam_page(self, exam):
        """
        Displays page before starting the exam.
        """
        exam_info = self.user.get_exam_info(exam)
        self.display_widget(StartExamPage(exam, exam_info, self.display_home_page, self.start_exam))

    @safe
    def login(self, group, user, password, ip_address):
        """
        Tries to login the student.
        """
        self.widget.set_waiting_state()
        password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        self.user.update_user_info(group, user, password)
        self.user.update_ip(ip_address)
        success = self.user.login()
        if not success:
            self.display_login_page('Попробуйте ещё раз')
            return
        self.display_home_page()

    @safe
    def start_exam(self, exam):
        """
        Starts the exam.
        """
        self.user.start_exam(exam)
        self.display_exam(exam)

    @safe
    def finish_exam(self, exam):
        """
        Finishes the exam.
        """
        self.user.finish_exam(exam)
        self.display_exam(exam)

    @safe
    def display_exam(self, exam):
        """
        Displays the exam depending on it's current state.
        """
        exam_info = self.user.get_exam_info(exam)
        if exam_info['state'] == 'Not started':
            self.display_start_exam_page(exam)
        else:
            self.display_widget(ExamPage(exam, self.display_home_page))
            self.view_question(exam, 1)

    @safe
    def view_question(self, exam, question):
        """
        Displays selected question.
        """
        exam_data = self.user.get_exam(exam)
        exam_info = self.user.get_exam_info(exam)
        self.widget.display(question, exam_data, exam_info, self.view_question,
                            self.get_exam_status_widget,
                            self.get_question_widget)

    @safe
    def get_exam_status_widget(self, parent):
        """
        Returns exam status widget.
        """
        if parent.exam_info['state'] == 'Running':
            return ExamRunning(parent, self.finish_exam)
        else:
            return ExamFinished(parent)

    @safe
    def get_question_widget(self, parent):
        """
        Returns the question widget depending on it's type.
        """
        question_data = parent.exam_data[parent.question - 1]
        if question_data['type'] == 'Short':
            if parent.exam_info['state'] == 'Finished':
                return QuestionShortDetails(parent)
            elif question_data['score'] is not False:
                return QuestionShortChecked(parent, self.view_question)
            else:
                return QuestionShort(parent, self.check_answer)
        elif question_data['type'] == 'Long':
            if parent.exam_info['state'] == 'Finished':
                return QuestionLongDetails(parent)
            else:
                return QuestionLong(parent, self.check_answer, self.view_question)

    @safe
    def check_answer(self, exam, question, answer):
        """
        Checks the student's answer and refreshes the page.
        """
        self.user.save_answer(exam, question, answer)
        self.user.check(exam, question)
        self.view_question(exam, question)


if __name__ == "__main__":
    APP = Application()
    APP.start()
