"""
Examiner project, student module
"""


import sys
from PyQt5.Qt import QApplication, QWidget, QHBoxLayout
import server
from login_page import LoginPage
from home_page import HomePage
from start_exam_page import StartExamPage
from exam_page import ExamPage
from exam_status import ExamRunning, ExamFinished
from question_short import QuestionShort, QuestionShortChecked, QuestionShortDetails


class Application(QApplication):
    """
    Main application class.
    """
    def __init__(self):
        super().__init__(sys.argv)
        self.group = ''
        self.user = ''
        self.password = ''
        self.server = None
        self.window = QWidget()
        self.window.setWindowTitle('Школьник')
        self.window.setGeometry(200, 100, 1000, 700)
        self.widget = QWidget(self.window)
        self.layout = QHBoxLayout(self.window)
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
        self.display_widget(LoginPage(self, self.login, server.read_ip()))
        self.exit(self.exec_())

    def display_login_page(self, status):
        """
        Displays login page for student.
        """
        self.display_widget(LoginPage(
            self, self.login, server.read_ip(), status=status))

    def display_home_page(self):
        """
        Displays home page with list of exams.
        """
        list_of_exams = server.list_of_exams(self)
        if list_of_exams is None:
            return
        self.display_widget(HomePage(self, list_of_exams, self.display_exam))

    def display_start_exam_page(self, exam):
        """
        Displays page before starting the exam.
        """
        exam_info = server.get_exam_info(self, exam)
        if exam_info is None:
            return
        self.display_widget(StartExamPage(exam, exam_info, self.display_home_page, self.start_exam))

    def login(self, group, user, password, ip_address):
        """
        Tries to login the student.
        """
        self.widget.set_waiting_state()
        self.group = group
        self.user = user
        self.password = password
        server.update_ip(self, ip_address)
        success = server.login(self)
        if success is None:
            return
        if not success:
            self.display_login_page('Данные неверны')
            return
        self.display_home_page()

    def start_exam(self, exam):
        """
        Starts the exam.
        """
        success = server.start_exam(self, exam)
        if success is not None:
            self.display_exam(exam)

    def finish_exam(self, exam):
        """
        Finishes the exam.
        """
        success = server.finish_exam(self, exam)
        if success is not None:
            self.display_exam(exam)

    def display_exam(self, exam):
        """
        Displays the exam depending on it's current state.
        """
        exam_info = server.get_exam_info(self, exam)
        if exam_info is None:
            return
        if exam_info['state'] == 'Not started':
            self.display_start_exam_page(exam)
        else:
            self.display_widget(ExamPage(exam, self.display_home_page))
            self.view_question(exam, 1)

    def view_question(self, exam, question):
        """
        Displays selected question.
        """
        exam_data = server.get_exam(self, exam)
        exam_info = server.get_exam_info(self, exam)
        if exam_data is None or exam_info is None:
            return
        self.widget.display(question, exam_data, exam_info, self.view_question,
                            self.get_exam_status_widget, self.get_question_widget)

    def get_exam_status_widget(self, parent):
        """
        Returns exam status widget.
        """
        if parent.exam_info['state'] == 'Running':
            return ExamRunning(parent, self.finish_exam)
        else:
            return ExamFinished(parent)

    def get_question_widget(self, parent):
        """
        Returns the question widget depending on it's type.
        """
        question_data = parent.exam_data[parent.question - 1]
        if question_data['type'] == 'Short':
            if parent.exam_info['state'] == 'Finished':
                return QuestionShortDetails(parent)
            elif question_data['score'] is not False:
                return QuestionShortChecked(parent, self.finish_exam, self.view_question)
            else:
                return QuestionShort(parent, self.check_answer)

    def check_answer(self, exam, question, answer):
        """
        Checks the student's answer and refreshes the page.
        """
        success = server.save_answer(self, exam, question, answer)
        if success is None:
            return
        success = server.check(self, exam, question)
        if success is None:
            return
        self.view_question(exam, question)


if __name__ == "__main__":
    APP = Application()
    APP.start()
