"""
Examiner project, student module.
Version 1.0
"""

import sys
import os
import time
import socket
from xmlrpc.client import ServerProxy
from PyQt5.Qt import Qt, QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.Qt import QLabel, QLineEdit, QScrollArea, QPushButton
from PyQt5.Qt import QFont, QPixmap, QSize, QSizePolicy, QSpacerItem, QFrame
from mywidgets import Label, Pixmap, Timer


def return_lambda(func, *args, **kwargs):
    """
    Returns lambda: func(*args, **kwargs)
    """
    return lambda: func(*args, **kwargs)


def read_ip():
    """
    Returns current ip-address of server.
    """
    return open('server.txt', encoding=ENCODING).read()


def update_ip(ip_address):
    """
    Updates current ip-address of server.
    """
    open('server.txt', 'w', encoding=ENCODING).write(ip_address)


def get_status(score, maxscore):
    """
    Returns color and picture depending on the result.
    """
    if score == maxscore:
        return {'color': '#6FCB36', 'picture': TICK50}
    else:
        return {'color': '#F10608', 'picture': CROSS50}


class QuestionShortDetails(QWidget):
    """
    Returns widget for details of short question.
    """
    def __init__(self, question, parent):
        super().__init__()
        question_data = parent.exam_data[question - 1]
        current_answer = question_data['answer'] if question_data['answer'] is not False else ''
        current_score = question_data['score'] if question_data['score'] is not False else '0'
        status = get_status(int(current_score), int(question_data['maxscore']))

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        statement_label = QLabel(question_data['statement'])
        statement_label.setFont(QFont('Arial', 20))
        statement_label.setWordWrap(True)

        your_answer_title = QLabel('Ваш ответ:')
        your_answer_title.setFont(QFont('Arial', 25))
        your_answer_title.setFixedWidth(300)

        your_answer_label = QLabel(current_answer)
        your_answer_label.setFont(QFont('Arial', 20))
        your_answer_label.setWordWrap(True)
        your_answer_label.setStyleSheet(
            'border-style: solid;'
            'border-width: 2px;'
            'border-color: ' + status['color'] + ';')

        status_img = QLabel()
        status_img.setPixmap(status['picture'])
        status_img.setFixedSize(QSize(50, 50))

        correct_answer_title = QLabel('Правильный ответ:')
        correct_answer_title.setFont(QFont('Arial', 25))
        correct_answer_title.setFixedWidth(300)

        correct_answer_label = QLabel(question_data['correct'])
        correct_answer_label.setFont(QFont('Arial', 20))
        correct_answer_label.setWordWrap(True)

        score_title = QLabel('Получено баллов:')
        score_title.setFont(QFont('Arial', 25))
        score_title.setFixedWidth(300)

        score_label = QLabel(current_score + ' (из ' + question_data['maxscore'] + ')')
        score_label.setFont(QFont('Arial', 25))

        your_answer_layout = QHBoxLayout()
        your_answer_layout.addWidget(your_answer_title)
        your_answer_layout.addSpacerItem(QSpacerItem(20, 0))
        your_answer_layout.addWidget(your_answer_label)
        your_answer_layout.addSpacerItem(QSpacerItem(10, 0))
        your_answer_layout.addWidget(status_img)

        correct_answer_layout = QHBoxLayout()
        correct_answer_layout.addWidget(correct_answer_title)
        correct_answer_layout.addSpacerItem(QSpacerItem(20, 0))
        correct_answer_layout.addWidget(correct_answer_label)
        correct_answer_layout.addStretch(1)

        score_layout = QHBoxLayout()
        score_layout.addWidget(score_title)
        score_layout.addSpacerItem(QSpacerItem(20, 0))
        score_layout.addWidget(score_label)
        score_layout.addStretch(1)

        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(statement_label)
        scroll_layout.addStretch(1)
        scroll_layout.addSpacerItem(QSpacerItem(0, 20))
        scroll_layout.addLayout(your_answer_layout)
        scroll_layout.addSpacerItem(QSpacerItem(0, 10))
        scroll_layout.addLayout(correct_answer_layout)
        scroll_layout.addSpacerItem(QSpacerItem(0, 10))
        scroll_layout.addLayout(score_layout)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class QuestionShortChecked(QWidget):
    """
    Returns widget for checked short question.
    """
    def __init__(self, question, parent):
        super().__init__()
        question_data = parent.exam_data[question - 1]
        status = get_status(int(question_data['score']), int(question_data['maxscore']))
        if question == len(parent.exam_data):
            next_text = 'Закончить'
            next_func = lambda: finish_exam(parent.exam)
        else:
            next_text = 'Далее'
            next_func = lambda: parent.display(question + 1)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        statement_label = QLabel(question_data['statement'])
        statement_label.setFont(QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = QLabel('Ответ:')
        answer_title.setFont(QFont('Arial', 30))

        answer_input = QLineEdit(question_data['answer'])
        answer_input.setFont(QFont('Arial', 20))
        answer_input.setDisabled(True)
        answer_input.setMinimumWidth(400)
        answer_input.setStyleSheet(
            'border-style: solid;'
            'border-width: 2px;'
            'border-color: ' + status['color'] + ';')

        status_img = QLabel()
        status_img.setPixmap(status['picture'])

        next_label = Label(next_text, normal_color='#2EBACB', hover_color='#2EBACB')
        next_label.setFont(QFont('Arial', 30))
        next_label.clicked.connect(next_func)

        next_img = Pixmap(normal_pic=RIGHT50, hover_pic=RIGHT50)
        next_img.clicked.connect(next_func)

        answer_layout = QHBoxLayout()
        answer_layout.addWidget(answer_title)
        answer_layout.addSpacerItem(QSpacerItem(20, 0))
        answer_layout.addWidget(answer_input)
        answer_layout.addSpacerItem(QSpacerItem(20, 0))
        answer_layout.addWidget(status_img)
        answer_layout.addStretch(1)
        answer_layout.addSpacerItem(QSpacerItem(20, 0))
        answer_layout.addWidget(next_label)
        answer_layout.addWidget(next_img)

        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(statement_label)
        scroll_layout.addStretch(1)
        scroll_layout.addSpacerItem(QSpacerItem(0, 20))
        scroll_layout.addLayout(answer_layout)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class QuestionShort(QWidget):
    """
    Returns widget for short question.
    """
    def __init__(self, question, parent):
        super().__init__()
        self.parent = parent
        self.question = question
        question_data = parent.exam_data[question - 1]

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        statement_label = QLabel(question_data['statement'])
        statement_label.setFont(QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = QLabel('Ответ:')
        answer_title.setFont(QFont('Arial', 30))

        answer_input = QLineEdit()
        answer_input.setFont(QFont('Arial', 20))
        answer_input.setMinimumWidth(400)

        check_label = Label('Проверить', normal_color='#2EBACB', hover_color='#2EBACB')
        check_label.setFont(QFont('Arial', 30))
        check_label.clicked.connect(lambda: self.check_answer(answer_input.text()))

        check_img = Pixmap(normal_pic=RIGHT50, hover_pic=RIGHT50)
        check_img.clicked.connect(lambda: self.check_answer(answer_input.text()))

        answer_layout = QHBoxLayout()
        answer_layout.addWidget(answer_title)
        answer_layout.addSpacerItem(QSpacerItem(20, 0))
        answer_layout.addWidget(answer_input)
        answer_layout.addStretch(1)
        answer_layout.addSpacerItem(QSpacerItem(20, 0))
        answer_layout.addWidget(check_label)
        answer_layout.addWidget(check_img)

        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(statement_label)
        scroll_layout.addStretch(1)
        scroll_layout.addSpacerItem(QSpacerItem(0, 10))
        scroll_layout.addLayout(answer_layout)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def check_answer(self, answer):
        """
        Checks the student's answer and refreshes the page.
        """
        APP.server.save_answer(APP.group, APP.user, self.parent.exam, self.question, answer)
        APP.server.check(APP.group, APP.user, self.parent.exam, self.question)
        self.parent.display(self.question)


def get_question_widget(question, parent):
    """
    Returns the question widget depending on it's type.
    """
    question_data = parent.exam_data[question - 1]
    if question_data['type'] == 'Short':
        if parent.exam_info['state'] == 'Finished':
            return QuestionShortDetails(question, parent)
        elif question_data['score'] is not False:
            return QuestionShortChecked(question, parent)
        else:
            return QuestionShort(question, parent)
    # TODO: Add other types!


def get_exam_status_widget(parent):
    """
    Returns exam status widget.
    """
    exam_info = parent.exam_info
    status_widget = QWidget()
    status_layout = QHBoxLayout()

    if exam_info['state'] == 'Running':
        info_label = QLabel('Экзамен идёт.')
        info_label.setFont(QFont('Arial', 25))

        timer_label = QLabel()
        timer_label.setFont(QFont('Arial', 25))
        APP.timer = Timer()
        APP.timer.tie(timer_label)
        APP.timer.start(int(exam_info['end']) - int(time.time()), lambda: finish_exam(parent.exam))

        status_layout.addWidget(info_label)
        status_layout.addStretch(1)
        status_layout.addWidget(timer_label)
    else:
        total_score = exam_info['total_score']
        total_maxscore = exam_info['total_maxscore']
        info_label = QLabel(
            'Экзамен завершён. Суммарный балл - ' +
            str(total_score) + ' (из ' + str(total_maxscore) + ')')
        info_label.setFont(QFont('Arial', 25))
        info_label.setWordWrap(True)
        status_layout.addWidget(info_label)

    status_widget.setLayout(status_layout)
    return status_widget


class ExamPage(QWidget):
    """
    Page that is displayed when student is passing the exam.
    """
    def __init__(self, exam):
        super().__init__()
        self.exam = exam
        self.exam_data = None
        self.exam_info = None

        back_img = Pixmap(normal_pic=LEFT50, hover_pic=LEFT50)
        back_img.setFixedSize(QSize(50, 50))
        back_img.clicked.connect(lambda: APP.display_page(HomePage))

        exam_title = QLabel(exam)
        exam_title.setFont(QFont('Arial', 30))
        exam_title.setAlignment(Qt.AlignCenter)
        exam_title.setWordWrap(True)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setMinimumHeight(85)
        scroll_area.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        status_widget = QWidget()
        question_widget = QWidget()

        self.questions_layout = QHBoxLayout()
        self.questions_layout.setSpacing(0)

        scroll_layout = QHBoxLayout()
        scroll_layout.addStretch(1)
        scroll_layout.addLayout(self.questions_layout)
        scroll_layout.addStretch(1)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        upper_layout = QHBoxLayout()
        upper_layout.addWidget(back_img)
        upper_layout.addWidget(exam_title)

        layout = QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(QSpacerItem(0, 10))
        layout.addWidget(scroll_area)
        layout.addWidget(status_widget)
        layout.addWidget(question_widget)
        self.setLayout(layout)

    def display(self, current_question):
        """
        Displays current question.
        """
        exam_data = APP.server.get_exam(APP.group, APP.user, self.exam)
        exam_info = APP.server.get_exam_info(APP.group, APP.user, self.exam)
        self.exam_data = exam_data
        self.exam_info = exam_info

        while self.questions_layout.count() > 0:
            old_widget = self.questions_layout.itemAt(0).widget()
            old_widget.deleteLater()
            self.questions_layout.removeWidget(old_widget)

        for question in range(1, len(exam_data) + 1):
            question_data = exam_data[question - 1]
            question_label = Label(str(question))
            question_label.setFont(QFont('Arial', 20))
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setFixedSize(QSize(50, 50))
            question_label.clicked.connect(return_lambda(self.display, question))

            self.questions_layout.addWidget(question_label)

            if question == current_question:
                question_label.setStyleSheet(
                    'color: blue;'
                    'background: #CCE8FF;'
                    'border-style: solid;'
                    'border-width: 1px;'
                    'border-color: #99D1FF')
            else:
                if question_data['score'] is False:
                    background = 'white'
                elif int(question_data['score']) == int(question_data['maxscore']):
                    background = '#9CFB8E' # correct
                else:
                    background = '#F94D51' # incorrect
                question_label.setStyleSheet(
                    'background: ' + background + ';'
                    'border-style: solid;'
                    'border-width: 1px')

        APP.timer.reset()
        status_widget = get_exam_status_widget(self)
        question_widget = get_question_widget(current_question, self)
        old_widget = self.layout().itemAt(4).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        old_widget = self.layout().itemAt(3).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        self.layout().addWidget(status_widget)
        self.layout().addWidget(question_widget)


class StartExamPage(QWidget):
    """
    Page before starting the exam.
    """
    def __init__(self, exam, exam_info):
        super().__init__()
        info_str = (
            'Информация об экзамене:\n\n'
            '    Продолжительность - ' + str(exam_info['duration']) + ' минут\n' +
            '    Количество заданий - ' + str(exam_info['quantity']) + '\n\n' +
            'Прервать выполнение заданий будет невозможно.\n'
            'Вы уверены, что хотите начать экзамен?')

        back_img = Pixmap(normal_pic=LEFT50, hover_pic=LEFT50)
        back_img.setFixedSize(QSize(50, 50))
        back_img.clicked.connect(lambda: APP.display_page(HomePage))

        exam_title = QLabel(exam)
        exam_title.setFont(QFont('Arial', 30))
        exam_title.setAlignment(Qt.AlignCenter)
        exam_title.setWordWrap(True)

        info_label = QLabel(info_str)
        info_label.setFont(QFont('Arial', 20))
        info_label.setWordWrap(True)

        start_button = QPushButton('Начать экзамен')
        start_button.setFont(QFont('Arial', 20))
        start_button.setMinimumSize(QSize(230, 50))
        start_button.clicked.connect(lambda: start_exam(exam))

        upper_layout = QHBoxLayout()
        upper_layout.addWidget(back_img)
        upper_layout.addWidget(exam_title)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(start_button)
        button_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(QSpacerItem(0, 20))
        layout.addWidget(info_label)
        layout.addSpacerItem(QSpacerItem(0, 20))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)


def start_exam(exam):
    """
    Starts the exam.
    """
    APP.server.start_exam(APP.group, APP.user, exam)
    display_exam(exam)


def finish_exam(exam):
    """
    Finishes the exam.
    """
    APP.server.finish_exam(APP.group, APP.user, exam)
    display_exam(exam)


def display_exam(exam):
    """
    Displays the exam depending on it's current state.
    """
    exam_info = APP.server.get_exam_info(APP.group, APP.user, exam)
    if exam_info['state'] == 'Not started':
        APP.display_page(StartExamPage, exam, exam_info)
    else:
        APP.display_page(ExamPage, exam).display(1)


class HomePage(QWidget):
    """
    Student's home page with list of exams.
    """
    def __init__(self):
        super().__init__()

        group_title = QLabel('Группа ' + APP.group)
        group_title.setFont(QFont('Arial', 30))
        group_title.setAlignment(Qt.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        scroll_layout = QVBoxLayout()

        for exam in APP.server.list_of_exams(APP.group):
            exam_image = QLabel()
            exam_image.setPixmap(EXAM30)
            exam_image.setFixedSize(QSize(30, 30))

            exam_label = Label(exam, normal_color='black', hover_color='blue')
            exam_label.setFont(QFont('Arial', 20))
            exam_label.setWordWrap(True)
            exam_label.clicked.connect(return_lambda(display_exam, exam))

            exam_layout = QHBoxLayout()
            exam_layout.addWidget(exam_image)
            exam_layout.addWidget(exam_label)

            scroll_layout.addLayout(exam_layout)
            scroll_layout.addSpacerItem(QSpacerItem(0, 10))

        scroll_layout.addStretch(1)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout()
        layout.addWidget(group_title)
        layout.addSpacerItem(QSpacerItem(0, 20))
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class LoginPage(QWidget):
    """
    Login page for student.
    """
    def __init__(self, status=''):
        super().__init__()

        enter_title = QLabel('Вход в систему')
        enter_title.setFont(QFont('Arial', 30))
        enter_title.setAlignment(Qt.AlignCenter)

        group_title = QLabel('Группа:')
        group_title.setFont(QFont('Arial', 20))

        group_input = QLineEdit(APP.group)
        group_input.setFont(QFont('Arial', 20))
        group_input.setMinimumWidth(400)
        group_input.setText('M20 История') # TODO: REMOVE THEN!

        user_title = QLabel('Логин:')
        user_title.setFont(QFont('Arial', 20))

        user_input = QLineEdit(APP.user)
        user_input.setFont(QFont('Arial', 20))
        user_input.setMinimumWidth(400)
        user_input.setText('Фёдор Куянов') # TODO: REMOVE THEN!

        password_title = QLabel('Пароль:')
        password_title.setFont(QFont('Arial', 20))

        password_input = QLineEdit(APP.password)
        password_input.setFont(QFont('Arial', 20))
        password_input.setMinimumWidth(400)
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setText('12345') # TODO: REMOVE THEN!

        enter_button = QPushButton('Войти в систему')
        enter_button.setFont(QFont('Arial', 20))
        enter_button.setMinimumSize(QSize(250, 50))
        enter_button.clicked.connect(lambda: self.login(
            group_input.text(), user_input.text(), password_input.text(), server_input.text()))

        self.status_label = QLabel(status)
        self.status_label.setFont(QFont('Arial', 20))
        self.status_label.setMinimumWidth(270)
        self.status_label.setStyleSheet('color: red')

        server_title = QLabel('IP-адрес сервера:')
        server_title.setFont(QFont('Arial', 15))

        server_input = QLineEdit(read_ip())
        server_input.setFont(QFont('Arial', 15))
        server_input.setMinimumWidth(300)
        server_input.setStyleSheet('background: #F0F0F0')

        title_layout = QVBoxLayout()
        title_layout.addWidget(group_title)
        title_layout.addSpacerItem(QSpacerItem(0, 20))
        title_layout.addWidget(user_title)
        title_layout.addSpacerItem(QSpacerItem(0, 20))
        title_layout.addWidget(password_title)

        input_layout = QVBoxLayout()
        input_layout.addWidget(group_input)
        input_layout.addSpacerItem(QSpacerItem(0, 20))
        input_layout.addWidget(user_input)
        input_layout.addSpacerItem(QSpacerItem(0, 20))
        input_layout.addWidget(password_input)

        main_layout = QHBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)
        main_layout.addStretch(1)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(enter_button)
        button_layout.addSpacerItem(QSpacerItem(20, 0))
        button_layout.addWidget(self.status_label)
        button_layout.addStretch(1)

        server_layout = QHBoxLayout()
        server_layout.addStretch(1)
        server_layout.addWidget(server_title)
        server_layout.addSpacerItem(QSpacerItem(20, 0))
        server_layout.addWidget(server_input)
        server_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addWidget(enter_title)
        layout.addStretch(1)
        layout.addLayout(main_layout)
        layout.addSpacerItem(QSpacerItem(0, 60))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        layout.addLayout(server_layout)
        self.setLayout(layout)

    def login(self, group, user, password, ip_address):
        """
        Tries to login the student.
        """
        self.setCursor(Qt.WaitCursor)
        self.status_label.setText('Подождите...')
        self.status_label.setStyleSheet('color: black')
        self.status_label.repaint()

        update_ip(ip_address)
        APP.server = ServerProxy('http://' + ip_address + ':8000')
        APP.group = group
        APP.user = user
        APP.password = password

        try:
            success = APP.server.login(group, user, password)
            if success:
                APP.display_page(HomePage)
            else:
                APP.display_page(LoginPage, status='Данные не верны')
        except socket.error:
            APP.display_page(LoginPage, status='Сервер не отвечает')


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
        self.timer = Timer()
        self.window = QWidget()
        self.window.setWindowTitle('Школьник')
        self.window.setGeometry(200, 100, 1000, 700)
        self.layout = QHBoxLayout(self.window)
        self.layout.addWidget(QWidget(self.window))
        self.window.show()

    def display_page(self, current_page, *args, **kwargs):
        """
        Displays and returns current_page(*args, **kwargs).
        """
        self.timer.reset()
        old_page = self.layout.itemAt(0).widget()
        new_page = current_page(*args, **kwargs)
        old_page.deleteLater()
        self.layout.removeWidget(old_page)
        self.layout.addWidget(new_page)
        return new_page


if __name__ == "__main__":
    APP = Application()
    ENCODING = 'utf-8-sig'
    EXAM30 = QPixmap(os.path.join('data', 'exam-30x30.png'))
    UPDATE50 = QPixmap(os.path.join('data', 'update-50x50.png'))
    LEFT50 = QPixmap(os.path.join('data', 'left-50x50.png'))
    RIGHT50 = QPixmap(os.path.join('data', 'right-50x50.png'))
    TICK50 = QPixmap(os.path.join('data', 'tick-50x50.png'))
    CROSS50 = QPixmap(os.path.join('data', 'cross-50x50.png'))

    APP.display_page(LoginPage)
    socket.setdefaulttimeout(3)
    sys.exit(APP.exec_())
