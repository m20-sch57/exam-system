"""
Examiner project, teacher module.
"""


import sys
import socket
import functools

from PyQt5 import Qt
from client import Client
from settings_page import SettingsPage
from login_page import LoginPage
from register_page import RegisterPage
from new_group_page import NewGroupPage
from home_page import HomePage
from profile_page import ProfilePage
from confirm_page import ConfirmPage
from error_widget import ErrorWidget
from exam_page import ExamPage
from exam_settings import ExamSettings
from question_short import QuestionShortEdit
from question_long import QuestionLongEdit
from results_page import ResultsPage
from student_answer_page import StudentAnswerPage


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
        self.client = Client()
        self.window = Qt.QWidget()
        self.window.setStyleSheet(open('client//style.css').read())
        self.window.setWindowTitle('Teacher')
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
            self.client.update_data({'server': ip_address})
            self.client.update_server()
            self.client.server.ping()
            self.widget.set_succeeded_state()
        except socket.error:
            self.widget.set_failed_state()

    def save_settings(self, settings):
        """
        Saves all settings.
        """
        self.client.set_data(settings)
        self.display_login_page()

    def display_settings_page(self):
        """
        Displays settings page.
        """
        self.display_widget(SettingsPage(self))

    def display_login_page(self):
        """
        Displays login page for teacher.
        """
        self.display_widget(LoginPage(self))

    def display_register_page(self):
        """
        Displays register page for teacher.
        """
        self.display_widget(RegisterPage(self))

    def display_new_group_page(self):
        """
        Displays page for creating new group.
        """
        self.display_widget(NewGroupPage(self))

    @safe
    def create_group(self, group_name):
        """
        Creates the group.
        """
        self.widget.set_waiting_state()
        result = self.client.server.create_group(group_name)
        if not result[0]:
            self.widget.set_failed_state(result[1])
        else:
            self.display_register_page()

    @safe
    def register(self, group_name, user_name, password):
        """
        Tries to register the teacher.
        """
        self.widget.set_waiting_state()
        password_hash = self.client.encode_password(password)
        result = self.client.server.register(user_name, password_hash, 1, group_name)
        if not result[0]:
            self.widget.set_failed_state(result[1])
        else:
            self.client.user_name = user_name
            self.client.password = password
            self.display_login_page()

    @safe
    def login(self, user_name, password):
        """
        Tries to login the teacher.
        """
        self.widget.set_waiting_state()
        self.client.user_name = user_name
        self.client.password = password
        password_hash = self.client.encode_password(password)
        result = self.client.server.login(user_name, password_hash, 1)
        if not result[0]:
            self.client.user = False
            self.widget.set_failed_state(result[1])
        else:
            self.client.user = result[1]
            self.display_home_page()

    @safe
    def logout(self):
        """
        Logs out the teacher.
        """
        self.client.user = False
        self.display_login_page()

    @safe
    def change_password(self, old_password, new_password):
        """
        Changes password of current user.
        """
        self.widget.set_waiting_state()
        old_password_hash = self.client.encode_password(old_password)
        new_password_hash = self.client.encode_password(new_password)
        result = self.client.server.change_password(
            self.client.user['rowid'], old_password_hash, new_password_hash)
        if not result[0]:
            self.widget.set_failed_state(result[1])
        else:
            self.client.password = new_password
            self.logout()

    def current_group_name(self):
        """
        Returns group name of current user.
        """
        return self.client.server.get_group_data(self.client.user['group_id'])['name']

    def list_of_exams(self):
        """
        Returns list of exams.
        """
        return self.client.server.list_of_all_exams(self.client.user['group_id'])

    @safe
    def display_home_page(self):
        """
        Displays home page with list of exams.
        """
        group_name = self.current_group_name()
        list_of_exams = self.list_of_exams()
        self.display_widget(HomePage(self, group_name, list_of_exams))

    @safe
    def display_profile_page(self):
        """
        Displays user profile.
        """
        group_name = self.current_group_name()
        user_name = self.client.user['name']
        self.display_widget(ProfilePage(self, group_name, user_name))

    @safe
    def display_exam(self, exam_id):
        """
        Displays the exam.
        """
        self.display_widget(ExamPage(self, exam_id))
        self.view_exam_settings()

    @safe
    def create_exam(self):
        """
        Creates the exam.
        """
        exam_id = self.client.server.create_exam(self.client.user['group_id'])
        self.display_exam(exam_id)

    @safe
    def delete_exam(self, exam_id):
        """
        Deletes the exam.
        """
        self.client.server.delete_exam(exam_id)
        self.display_home_page()

    def display_confirm_page(self, text, back_function, main_function):
        """
        Displays confirmation page.
        """
        self.display_widget(ConfirmPage(text, back_function, main_function))

    @safe
    def view_exam_settings(self):
        """
        Displays exam settings.
        """
        exam_id = self.widget.exam_id
        self.widget.question_id = None
        self.widget.exam_data = self.client.server.get_exam_data(exam_id)
        self.widget.questions_ids = self.client.server.get_questions_ids(exam_id)
        self.widget.refresh()
        self.widget.display_current_settings()

    @safe
    def view_exam_question(self, question_id):
        """
        Displays selected question.
        """
        exam_id = self.widget.exam_id
        self.widget.question_id = question_id
        self.widget.question_data = self.client.server.get_question_data(question_id)
        self.widget.questions_ids = self.client.server.get_questions_ids(exam_id)
        self.widget.refresh()
        self.widget.display_current_question()

    def get_settings_widget(self):
        """
        Returns the settings widget for the exam.
        """
        if not self.widget.exam_data:
            return ErrorWidget()
        return ExamSettings(self, self.widget)

    def get_question_widget(self):
        """
        Returns the question widget depending on it's type.
        """
        if not self.widget.question_data:
            return ErrorWidget()
        if self.widget.question_data['type'] == 'Short':
            return QuestionShortEdit(self, self.widget)
        if self.widget.question_data['type'] == 'Long':
            return QuestionLongEdit(self, self.widget)
        return ErrorWidget()

    @safe
    def create_question(self, exam_id, question_type):
        """
        Creates question with this type.
        """
        question_id = self.client.server.create_question(exam_id, question_type)
        self.view_exam_question(question_id)

    @safe
    def delete_question(self, question_id):
        """
        Deletes question.
        """
        self.client.server.delete_question(question_id)
        self.view_exam_settings()

    @safe
    def save_exam_data(self, exam_data):
        """
        Saves exam's settings.
        """
        self.client.server.set_exam_data(exam_data)
        self.view_exam_settings()
        self.widget.widget.update_status()

    @safe
    def save_question_data(self, question_data):
        """
        Saves exam's question.
        """
        question_id = question_data['rowid']
        self.client.server.set_question_data(question_data)
        self.view_exam_question(question_id)
        self.widget.widget.update_status()

    @safe
    def display_results_page(self, exam_id):
        """
        Displays results table of the exam.
        """
        users = self.client.server.get_users_by_exam(exam_id)
        questions_ids = self.client.server.get_questions_ids(exam_id)
        results_table = self.client.server.get_results_table(exam_id)
        self.display_widget(ResultsPage(self, exam_id, users, questions_ids, results_table))

    @safe
    def display_student_answer_page(self, exam_id, question_id, user_id):
        """
        Page to display student's answer for the question.
        """
        question_data = self.client.server.get_question_data(question_id)
        question_result = self.client.server.get_question_result(question_id, user_id)
        self.display_widget(StudentAnswerPage(self, exam_id, question_data, question_result))

    @safe
    def save_submission_score(self, exam_id, question_id, submission_id, score):
        """
        Saves score (share) of the submission.
        """
        question_data = self.client.server.get_question_data(question_id)
        share = -1 if score == '?' else int(score) / question_data['maxscore']
        self.client.server.save_submission_score(submission_id, share)
        self.display_results_page(exam_id)


if __name__ == "__main__":
    APP = Application()
    APP.start()
