from xmlrpc.client import *
from PyQt5.Qt import *
import socket


def return_lambda(func, *args, **kwargs):
    return lambda: func(*args, **kwargs)


def read_ip():
    return open('server.txt', encoding=ENCODING).read()


def write_ip(ip):
    print(ip, end='', file=open('server.txt', 'w', encoding=ENCODING))


def try_connect():
    global server

    ip = read_ip()
    try:
        server = ServerProxy('http://' + ip + ':8000')
        server.check_connection()
        return True
    except:
        return False


def display_page(page, *args, **kwargs):
    timer.reset()
    old_page = main_window_layout.itemAt(0).widget()
    main_window_layout.removeWidget(old_page)
    main_window_layout.addWidget(page(*args, **kwargs))
    old_page.deleteLater()


def logout():
    global global_group_name, global_user_name
    global_group_name = ''
    global_user_name = ''
    display_page(LoginPage)


class Timer:
    def __init__(self, timer_label):
        self.timer_label = timer_label
        self.current_time = -1

    def tick(self, func):
        if self.current_time > 0:
            self.current_time -= 1
            minutes, seconds = self.current_time // 60, self.current_time % 60
            if self.timer_label is not None:
                self.timer_label.setText('%02d:%02d' % (minutes, seconds))
                if self.current_time < 10:
                    self.timer_label.setStyleSheet('color: red')
            QTimer().singleShot(1000, lambda: self.tick(func))
        elif self.current_time == 0:
            func()

    def start(self, duration_time, func, *args, **kwargs):
        self.current_time = duration_time
        self.tick(func)

    def reset(self):
        self.current_time = -1


class QLabelClick(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text, normal_color='black', hover_color='blue'):
        QLabel.__init__(self, text)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('color: ' + normal_color)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.mousePressEvent = lambda event: self.clicked.emit()
        self.enterEvent = lambda event: self.setStyleSheet('color: ' + self.hover_color)
        self.leaveEvent = lambda event: self.setStyleSheet('color: ' + self.normal_color)


class QLabelPixMapClick(QLabel):
    clicked = pyqtSignal()

    def __init__(self, normal_pic, hover_pic):
        QLabel.__init__(self)
        self.setCursor(Qt.PointingHandCursor)
        self.setPixmap(QPixmap(normal_pic))
        self.normal_pic = normal_pic
        self.hover_pic = hover_pic
        self.mousePressEvent = lambda event: self.clicked.emit()
        self.enterEvent = lambda event: self.setPixmap(QPixmap(self.hover_pic))
        self.leaveEvent = lambda event: self.setPixmap(QPixmap(self.normal_pic))


class DetailsTestPage(QWidget):
    def __init__(self, exam_name, question_number, details):
        super().__init__(main_window)
        question = details[question_number - 1]

        global_layout = QVBoxLayout()

        back_label = QLabelPixMapClick('data\\left-50x50.png', 'data\\left-50x50.png')
        back_label.setFixedSize(QSize(50, 50))
        back_label.clicked.connect(lambda: display_page(SummaryPage, exam_name, details))

        question_label = QLabel('Вопрос ' + str(question_number))
        question_label.setFont(QFont('Arial', 30))

        top_layout = QHBoxLayout()
        top_layout.addWidget(back_label)
        top_layout.addStretch(1)
        top_layout.addWidget(question_label)
        top_layout.addStretch(1)

        global_layout.addLayout(top_layout)
        global_layout.addItem(QSpacerItem(0, 20))

        statement_label = QLabel(question['statement'])
        statement_label.setFont(QFont('Arial', 20))
        statement_label.setWordWrap(True)

        global_layout.addWidget(statement_label)
        global_layout.addStretch(1)

        self.setLayout(global_layout)


class SummaryPage(QWidget):
    def __init__(self, exam_name, details):
        super().__init__(main_window)

        global_layout = QVBoxLayout()

        back_label = QLabelPixMapClick('data\\left-50x50.png', 'data\\left-50x50.png')
        back_label.setFixedSize(QSize(50, 50))
        back_label.clicked.connect(lambda: display_page(MainPage))

        results_label = QLabel('Результаты')
        results_label.setFont(QFont('Arial', 30))

        update_label = QLabelPixMapClick('data\\update-50x50.png', 'data\\update-50x50.png')
        update_label.setFixedSize(QSize(50, 50))
        update_label.clicked.connect(lambda: display_page(WaitingPage, exam_name))

        top_layout = QHBoxLayout()
        top_layout.addWidget(back_label)
        top_layout.addStretch(1)
        top_layout.addWidget(results_label)
        top_layout.addStretch(1)
        top_layout.addWidget(update_label)

        global_layout.addLayout(top_layout)
        global_layout.addItem(QSpacerItem(0, 20))

        score = 0
        max_score = 0
        scroll_layout = QVBoxLayout()
        for i in range(len(details)):
            score += details[i]['score']
            max_score += details[i]['max']

            question_label = QLabel('Вопрос ' + str(i + 1) + ':')
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setFont(QFont('Arial', 25))
            question_label.setFixedWidth(180)

            status_img_label = QLabel()
            status_img_label.setFixedSize(QSize(40, 40))

            score_label = QLabel('Балл: ' + str(details[i]['score']) + ' (из ' + str(details[i]['max']) + ')')
            score_label.setFont(QFont('Arial', 20))

            if details[i]['score'] == 0:
                status_img_label.setPixmap(QPixmap('data\\cross-40x40.png'))
            elif details[i]['score'] == details[i]['max']:
                status_img_label.setPixmap(QPixmap('data\\tick-40x40.png'))

            details_button = QPushButton('Просмотр')
            details_button.setFont(QFont('Arial', 20))
            details_button.setMinimumSize(QSize(150, 40))
            details_button.clicked.connect(return_lambda(display_page, DetailsTestPage, exam_name, i + 1, details))

            question_layout = QHBoxLayout()
            question_layout.addWidget(question_label)
            question_layout.addWidget(status_img_label)
            question_layout.addItem(QSpacerItem(20, 0))
            question_layout.addWidget(score_label)
            question_layout.addStretch(1)
            question_layout.addWidget(details_button)

            scroll_layout.addLayout(question_layout)

        scroll_layout.addStretch(1)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setFrameShape(QFrame.NoFrame)

        global_layout.addWidget(scroll_area)
        global_layout.addItem(QSpacerItem(0, 20))

        score_label = QLabel('Ваш балл: ' + str(score) + ' (из ' + str(max_score) + ')')
        score_label.setFont(QFont('Arial', 20))

        table_results_label = QLabelClick('Таблица результатов')
        table_results_label.setFont(QFont('Arial', 20))

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(score_label)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(table_results_label)

        global_layout.addLayout(bottom_layout)

        self.setLayout(global_layout)


class QuestionShortCheckedPage(QWidget):
    def __init__(self, exam_name, question_number, question, answer):
        super().__init__(main_window)
        result = server.check(global_group_name, global_user_name, exam_name, question_number, answer)

        global_layout = QVBoxLayout()

        question_label = QLabel('Вопрос ' + str(question_number))
        question_label.setAlignment(Qt.AlignCenter)
        question_label.setFont(QFont('Arial', 30))

        global_layout.addWidget(question_label)
        global_layout.addItem(QSpacerItem(0, 20))

        statement_label = QLabel(question['statement'])
        statement_label.setFont(QFont('Arial', 20))
        statement_label.setWordWrap(True)

        global_layout.addWidget(statement_label)
        global_layout.addStretch(1)

        answer_label = QLabel('Ваш ответ:')
        answer_label.setAlignment(Qt.AlignCenter)
        answer_label.setFont(QFont('Arial', 30))

        global_layout.addWidget(answer_label)
        global_layout.addItem(QSpacerItem(0, 20))

        answer_edit = QLineEdit(answer)
        answer_edit.setFont(QFont('Arial', 20))
        answer_edit.setDisabled(True)

        if result['score'] == 0:
            answer_edit.setStyleSheet('border-width: 2px;'
                                      'border-style: solid;'
                                      'border-color: ' + RED)
        else:
            answer_edit.setStyleSheet('border-width: 2px;'
                                      'border-style: solid;'
                                      'border-color: ' + GREEN)

        global_layout.addWidget(answer_edit)
        global_layout.addItem(QSpacerItem(0, 20))

        status_img_label = QLabel()
        status_img_label.setFixedSize(QSize(50, 50))

        status_label = QLabel()
        status_label.setFont(QFont('Arial', 30))

        if result['score'] == 0:
            status_img_label.setPixmap(QPixmap('data\\cross-50x50.png'))
            status_label.setText('Неправильно')
            status_label.setStyleSheet('color: ' + RED)
        else:
            status_img_label.setPixmap(QPixmap('data\\tick-50x50.png'))
            status_label.setText('Правильно')
            status_label.setStyleSheet('color: ' + GREEN)

        next_label = QLabelClick('Далее', normal_color=BLUE, hover_color=BLUE)
        next_label.setAlignment(Qt.AlignCenter)
        next_label.setFont(QFont('Arial', 30))
        next_label.setFixedSize(QSize(130, 50))
        next_label.clicked.connect(lambda: display_page(WaitingPage, exam_name, question_number + 1))

        next_img_label = QLabelPixMapClick('data\\right-50x50.png', 'data\\right-50x50.png')
        next_img_label.setFixedSize(QSize(50, 50))
        next_img_label.clicked.connect(lambda: display_page(WaitingPage, exam_name, question_number + 1))

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(0)
        bottom_layout.addWidget(status_img_label)
        bottom_layout.addItem(QSpacerItem(10, 0))
        bottom_layout.addWidget(status_label)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(next_label)
        bottom_layout.addWidget(next_img_label)

        global_layout.addLayout(bottom_layout)

        self.setLayout(global_layout)


class QuestionShortPage(QWidget):
    def __init__(self, exam_name, question_number, question):
        global timer

        super().__init__(main_window)

        global_layout = QVBoxLayout()

        question_label = QLabel('Вопрос ' + str(question_number))
        question_label.setFont(QFont('Arial', 30))

        timer_label = QLabel()
        timer_label.setFont(QFont('Arial', 30))

        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addWidget(question_label)
        top_layout.addStretch(1)
        top_layout.addWidget(timer_label)

        global_layout.addLayout(top_layout)
        global_layout.addItem(QSpacerItem(0, 20))

        statement_label = QLabel(question['statement'])
        statement_label.setFont(QFont('Arial', 20))
        statement_label.setWordWrap(True)

        global_layout.addWidget(statement_label)
        global_layout.addStretch(1)

        answer_label = QLabel('Ваш ответ:')
        answer_label.setAlignment(Qt.AlignCenter)
        answer_label.setFont(QFont('Arial', 30))

        global_layout.addWidget(answer_label)
        global_layout.addItem(QSpacerItem(0, 20))

        answer_edit = QLineEdit()
        answer_edit.setFont(QFont('Arial', 20))

        global_layout.addWidget(answer_edit)
        global_layout.addItem(QSpacerItem(0, 20))

        next_label = QLabelClick('Проверить', normal_color=BLUE, hover_color=BLUE)
        next_label.setAlignment(Qt.AlignCenter)
        next_label.setFont(QFont('Arial', 30))
        next_label.setFixedSize(QSize(210, 50))
        next_label.clicked.connect(lambda: display_page(
            QuestionShortCheckedPage, exam_name, question_number, question, answer_edit.text()))

        next_img_label = QLabelPixMapClick('data\\right-50x50.png', 'data\\right-50x50.png')
        next_img_label.setFixedSize(QSize(50, 50))
        next_img_label.clicked.connect(lambda: display_page(
            QuestionShortCheckedPage, exam_name, question_number, question, answer_edit.text()))

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(0)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(next_label)
        bottom_layout.addWidget(next_img_label)

        global_layout.addLayout(bottom_layout)

        self.setLayout(global_layout)

        timer = Timer(timer_label)
        timer.start(question['time'], lambda: display_page(
            QuestionShortCheckedPage, exam_name, question_number, question, answer_edit.text()))


class QuestionTestCheckedPage(QWidget):
    def __init__(self, exam_name, question_number, question, answer):
        super().__init__(main_window)
        result = server.check(global_group_name, global_user_name, exam_name, question_number, answer)

        global_layout = QVBoxLayout()

        question_label = QLabel('Вопрос ' + str(question_number))
        question_label.setAlignment(Qt.AlignCenter)
        question_label.setFont(QFont('Arial', 30))

        global_layout.addWidget(question_label)
        global_layout.addItem(QSpacerItem(0, 20))

        statement_label = QLabel(question['statement'])
        statement_label.setFont(QFont('Arial', 20))
        statement_label.setWordWrap(True)

        global_layout.addWidget(statement_label)
        global_layout.addStretch(1)

        variants_layout = QVBoxLayout()

        for i in range(len(question['variants'])):
            cur_img_label = QLabel()
            cur_img_label.setPixmap(QPixmap('data\\triangle-50x50.png'))
            cur_img_label.setFixedSize(QSize(50, 50))

            cur_label = QLabel(question['variants'][i])
            cur_label.setFont(QFont('Arial', 20))
            cur_label.setWordWrap(True)

            if answer == i + 1:
                if result['score'] == 0:
                    cur_img_label.setPixmap(QPixmap('data\\cross-50x50.png'))
                    cur_label.setStyleSheet('color: ' + RED + ';'
                                            'background: white; '
                                            'border-width: 2px;'
                                            'border-style: solid;'
                                            'border-color: ' + RED)
                else:
                    cur_img_label.setPixmap(QPixmap('data\\tick-50x50.png'))
                    cur_label.setStyleSheet('color: ' + GREEN + ';'
                                            'background: white; '
                                            'border-width: 2px;'
                                            'border-style: solid;'
                                            'border-color: ' + GREEN)

            cur_layout = QHBoxLayout()
            cur_layout.addWidget(cur_img_label)
            cur_layout.addWidget(cur_label)

            variants_layout.addLayout(cur_layout)

        global_layout.addLayout(variants_layout)
        global_layout.addItem(QSpacerItem(0, 20))

        status_img_label = QLabel()
        status_img_label.setFixedSize(QSize(50, 50))

        status_label = QLabel()
        status_label.setFont(QFont('Arial', 30))

        if result['score'] == 0:
            status_img_label.setPixmap(QPixmap('data\\cross-50x50.png'))
            status_label.setText('Неправильно')
            status_label.setStyleSheet('color: ' + RED)
        else:
            status_img_label.setPixmap(QPixmap('data\\tick-50x50.png'))
            status_label.setText('Правильно')
            status_label.setStyleSheet('color: ' + GREEN)

        next_label = QLabelClick('Далее', normal_color=BLUE, hover_color=BLUE)
        next_label.setAlignment(Qt.AlignCenter)
        next_label.setFont(QFont('Arial', 30))
        next_label.setFixedSize(QSize(130, 50))
        next_label.clicked.connect(lambda: display_page(WaitingPage, exam_name, question_number + 1))

        next_img_label = QLabelPixMapClick('data\\right-50x50.png', 'data\\right-50x50.png')
        next_img_label.setFixedSize(QSize(50, 50))
        next_img_label.clicked.connect(lambda: display_page(WaitingPage, exam_name, question_number + 1))

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(0)
        bottom_layout.addWidget(status_img_label)
        bottom_layout.addItem(QSpacerItem(10, 0))
        bottom_layout.addWidget(status_label)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(next_label)
        bottom_layout.addWidget(next_img_label)

        global_layout.addLayout(bottom_layout)

        self.setLayout(global_layout)


class QuestionTestPage(QWidget):
    def __init__(self, exam_name, question_number, question):
        global timer

        super().__init__(main_window)

        global_layout = QVBoxLayout()

        question_label = QLabel('Вопрос ' + str(question_number))
        question_label.setFont(QFont('Arial', 30))

        timer_label = QLabel()
        timer_label.setFont(QFont('Arial', 30))

        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addWidget(question_label)
        top_layout.addStretch(1)
        top_layout.addWidget(timer_label)

        global_layout.addLayout(top_layout)
        global_layout.addItem(QSpacerItem(0, 20))

        statement_label = QLabel(question['statement'])
        statement_label.setFont(QFont('Arial', 20))
        statement_label.setWordWrap(True)

        global_layout.addWidget(statement_label)
        global_layout.addStretch(1)

        variants_layout = QVBoxLayout()

        for i in range(len(question['variants'])):
            var_img_label = QLabel()
            var_img_label.setPixmap(QPixmap('data\\triangle-50x50.png'))
            var_img_label.setFixedSize(QSize(50, 50))

            var_label = QLabelClick(question['variants'][i])
            var_label.setFont(QFont('Arial', 20))
            var_label.setWordWrap(True)
            var_label.clicked.connect(return_lambda(
                display_page, QuestionTestCheckedPage, exam_name, question_number, question, i + 1))

            var_layout = QHBoxLayout()
            var_layout.addWidget(var_img_label)
            var_layout.addWidget(var_label)

            variants_layout.addLayout(var_layout)

        global_layout.addLayout(variants_layout)
        global_layout.addItem(QSpacerItem(0, 76))

        self.setLayout(global_layout)

        timer = Timer(timer_label)
        timer.start(question['time'], lambda: display_page(
            QuestionTestCheckedPage, exam_name, question_number, question, 0))


class WaitingPage(QWidget):
    def __init__(self, exam_name, question_number=-1):
        global timer

        super().__init__(main_window)

        if question_number == -1:
            question_number = server.first_not_passed_question(global_group_name, global_user_name, exam_name)

        if question_number <= server.number_of_questions(global_group_name, exam_name):
            global_layout = QVBoxLayout()

            question_label = QLabel('Вопрос ' + str(question_number))
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setFont(QFont('Arial', 50))

            global_layout.addWidget(question_label)

            self.setLayout(global_layout)

            question = server.view_question(global_group_name, global_user_name, exam_name, question_number)
            timer = Timer(None)
            if question['type'] == 'Тест':
                timer.start(1, lambda: display_page(QuestionTestPage, exam_name, question_number, question))
            elif question['type'] == 'Короткий ответ':
                timer.start(1, lambda: display_page(QuestionShortPage, exam_name, question_number, question))
            elif question['type'] == 'Развёрнутый ответ':
                timer.start(1, lambda: display_page(QuestionLongPage, exam_name, question_number, question))

        else:
            global_layout = QVBoxLayout()

            results_label = QLabel('Результаты')
            results_label.setAlignment(Qt.AlignCenter)
            results_label.setFont(QFont('Arial', 50))

            global_layout.addStretch(1)
            global_layout.addWidget(results_label)
            global_layout.addStretch(1)

            self.setLayout(global_layout)

            details = []
            for question_number in range(1, server.number_of_questions(global_group_name, exam_name) + 1):
                details.append(server.view_details(global_group_name, global_user_name, exam_name, question_number))
            timer = Timer(None)
            timer.start(1, lambda: display_page(SummaryPage, exam_name, details))


class MainPage(QWidget):
    def __init__(self):
        super().__init__(main_window)

        global_layout = QVBoxLayout()

        group_label = QLabel('Группа "' + global_group_name + '"')
        group_label.setAlignment(Qt.AlignCenter)
        group_label.setFont(QFont('Arial', 30))

        global_layout.addWidget(group_label)
        global_layout.addItem(QSpacerItem(0, 20))

        scroll_layout = QVBoxLayout()
        for exam_name in server.list_of_exams(global_group_name):
            var_img_label = QLabel()
            var_img_label.setPixmap(QPixmap('data\\exam-30x30.png'))
            var_img_label.setFixedSize(QSize(30, 30))

            var_label = QLabelClick(exam_name)
            var_label.setFont(QFont('Arial', 20))
            var_label.setWordWrap(True)
            var_label.clicked.connect(return_lambda(display_page, WaitingPage, exam_name))

            var_layout = QHBoxLayout()
            var_layout.addWidget(var_img_label)
            var_layout.addWidget(var_label)

            scroll_layout.addLayout(var_layout)
            scroll_layout.addItem(QSpacerItem(0, 10))

        scroll_layout.addStretch(1)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setFrameShape(QFrame.NoFrame)

        global_layout.addWidget(scroll_area)
        global_layout.addItem(QSpacerItem(0, 20))

        user_label = QLabel('Вы зашли как ' + global_user_name)
        user_label.setFont(QFont('Arial', 20))

        exit_label = QLabelClick('Выход')
        exit_label.setFont(QFont('Arial', 20))
        exit_label.clicked.connect(lambda: logout())

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(user_label)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(exit_label)

        global_layout.addLayout(bottom_layout)

        self.setLayout(global_layout)


class LoginPage(QWidget):
    def __init__(self, state=''):
        super().__init__(main_window)

        global_layout = QVBoxLayout()

        enter_label = QLabel('Вход в систему')
        enter_label.setAlignment(Qt.AlignCenter)
        enter_label.setFont(QFont('Arial', 30))

        global_layout.addWidget(enter_label)
        global_layout.addStretch(1)

        group_label = QLabel('Название группы:')
        group_label.setFont(QFont('Arial', 20))

        user_label = QLabel('Имя пользователя:')
        user_label.setFont(QFont('Arial', 20))

        left_layout = QVBoxLayout()
        left_layout.addWidget(group_label)
        left_layout.addItem(QSpacerItem(0, 20))
        left_layout.addWidget(user_label)

        group_edit = QLineEdit()
        group_edit.setFont(QFont('Arial', 20))
        group_edit.setText('M20 История')  # TODO: REMOVE THEN!!
        group_edit.setMinimumWidth(400)
        #group_edit.setText(global_group_name)

        user_edit = QLineEdit()
        user_edit.setFont(QFont('Arial', 20))
        user_edit.setText('Фёдор Куянов')  # TODO: REMOVE THEN!!
        user_edit.setMinimumWidth(400)
        #user_edit.setText(global_user_name)

        right_layout = QVBoxLayout()
        right_layout.addWidget(group_edit)
        right_layout.addItem(QSpacerItem(0, 20))
        right_layout.addWidget(user_edit)

        main_layout = QHBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(left_layout)
        main_layout.addItem(QSpacerItem(20, 0))
        main_layout.addLayout(right_layout)
        main_layout.addStretch(1)

        global_layout.addLayout(main_layout)
        global_layout.addItem(QSpacerItem(0, 70))

        enter_button = QPushButton('Войти в систему')
        enter_button.setFont(QFont('Arial', 20))
        enter_button.setMinimumSize(QSize(250, 50))

        self.status_label = QLabel(state)
        self.status_label.setFont(QFont('Arial', 20))
        self.status_label.setStyleSheet('color: red')
        self.status_label.setMinimumWidth(400)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(enter_button)
        button_layout.addItem(QSpacerItem(20, 0))
        button_layout.addWidget(self.status_label)
        button_layout.addStretch(1)

        global_layout.addLayout(button_layout)
        global_layout.addStretch(1)

        server_label = QLabel('IP-адрес сервера:')
        server_label.setFont(QFont('Arial', 15))

        server_edit = QLineEdit()
        server_edit.setFont(QFont('Arial', 15))
        server_edit.setText(read_ip())
        server_edit.setMinimumWidth(300)
        server_edit.setStyleSheet('Background: #f0f0f0')

        server_layout = QHBoxLayout()
        server_layout.addStretch(1)
        server_layout.addWidget(server_label)
        server_layout.addItem(QSpacerItem(20, 0))
        server_layout.addWidget(server_edit)
        server_layout.addStretch(1)

        global_layout.addLayout(server_layout)

        self.setLayout(global_layout)

        enter_button.clicked.connect(
            lambda: self.try_to_login(server_edit.text(), group_edit.text(), user_edit.text()))

    def try_to_login(self, ip, group_name, user_name):
        global server, global_group_name, global_user_name

        write_ip(ip)
        global_group_name = group_name
        global_user_name = user_name

        self.status_label.setText('Подождите...')
        self.status_label.setStyleSheet('color: black')
        self.status_label.repaint()
        self.setCursor(QCursor(Qt.WaitCursor))

        if not try_connect():
            display_page(LoginPage, state='Сервер не отвечает')
            return
        global_group_name = server.search_group(group_name)
        if not global_group_name:
            display_page(LoginPage, state='Неверное название группы')
            return
        global_user_name = server.search_user(global_group_name, user_name)
        if not global_user_name:
            display_page(LoginPage, state='Неверное имя пользователя')
            return
        display_page(MainPage)


if __name__ == "__main__":
    GREEN = '#6FCB36'
    RED = '#F10608'
    BLUE = '#2EBACB'
    ENCODING = 'utf-8-sig'
    global_group_name = ''
    global_user_name = ''
    timer = Timer(None)
    socket.setdefaulttimeout(3)

    app = QApplication(sys.argv)

    main_window = QWidget()
    main_window.setWindowTitle('Student')
    main_window.setGeometry(200, 100, 800, 600)

    main_window_layout = QHBoxLayout(main_window)
    main_window_layout.addWidget(LoginPage())

    main_window.show()
    sys.exit(app.exec_())
