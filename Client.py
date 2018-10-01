from xmlrpc.client import *
from PyQt5.Qt import *
import socket


def return_lambda(func, *args, **kwargs):
    return lambda: func(*args, **kwargs)


def read_ip():
    return open('server.txt', encoding=encoding).read()


def write_ip(ip):
    print(ip, end='', file=open('server.txt', 'w', encoding=encoding))


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
    old_page = main_window_layout.itemAt(0).widget()
    timer.reset()
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

    def tick(self, func, *args, **kwargs):
        if self.current_time > 0:
            self.current_time -= 1
            minutes, seconds = self.current_time // 60, self.current_time % 60
            if self.timer_label is not None:
                self.timer_label.setText('%02d:%02d' % (minutes, seconds))
            QTimer().singleShot(1000, lambda: self.tick(func, *args, **kwargs))
        elif self.current_time == 0:
            func(*args, **kwargs)

    def start(self, duration_time, func, *args, **kwargs):
        self.current_time = duration_time
        self.tick(func, *args, **kwargs)

    def reset(self):
        self.current_time = -1


class QLabelClick(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text):
        QLabel.__init__(self, text)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def enterEvent(self, event):
        self.setStyleSheet('color: blue')

    def leaveEvent(self, event):
        self.setStyleSheet('color: black')


class QLabelPixMapClick(QLabel):
    clicked = pyqtSignal()

    def __init__(self, normal_pic, hover_pic):
        QLabel.__init__(self)
        self.setPixmap(QPixmap(normal_pic))
        self.normal_pic = normal_pic
        self.hover_pic = hover_pic

    def mousePressEvent(self, event):
        self.clicked.emit()

    def enterEvent(self, event):
        self.setPixmap(QPixmap(self.hover_pic))

    def leaveEvent(self, event):
        self.setPixmap(QPixmap(self.normal_pic))


class QuestionTestCheckedPage(QWidget):
    def __init__(self, exam_name, question_number, question, answer):
        super().__init__(main_window)

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

        result = server.check(global_group_name, global_user_name, exam_name, question_number, answer)
        variants_layout = QVBoxLayout()
        for i in range(len(question['variants'])):
            img_label = QLabel()
            img_label.setPixmap(QPixmap('data\\triangle-50x50.png'))
            img_label.setFixedSize(QSize(50, 50))

            cur_label = QLabel(question['variants'][i])
            cur_label.setFont(QFont('Arial', 20))
            cur_label.setWordWrap(True)

            if answer == i + 1:
                if result['score'] == 0:
                    img_label.setPixmap(QPixmap('data\\cross-50x50.png'))
                    cur_label.setStyleSheet('color: ' + red_color + ';'
                                            'background: white; '
                                            'border-width: 2px;'
                                            'border-style: solid;'
                                            'border-color: ' + red_color)
                else:
                    img_label.setPixmap(QPixmap('data\\tick-50x50.png'))
                    cur_label.setStyleSheet('color: ' + green_color + ';'
                                            'background: white; '
                                            'border-width: 2px;'
                                            'border-style: solid;'
                                            'border-color: ' + green_color)

            cur_layout = QHBoxLayout()
            cur_layout.addWidget(img_label)
            cur_layout.addWidget(cur_label)

            variants_layout.addLayout(cur_layout)

        global_layout.addLayout(variants_layout)
        global_layout.addItem(QSpacerItem(0, 70))

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
            img_label = QLabel()
            img_label.setPixmap(QPixmap('data\\triangle-50x50.png'))
            img_label.setFixedSize(QSize(50, 50))

            cur_label = QLabelClick(question['variants'][i])
            cur_label.setFont(QFont('Arial', 20))
            cur_label.setWordWrap(True)
            cur_label.clicked.connect(return_lambda(
                display_page, QuestionTestCheckedPage, exam_name, question_number, question, i + 1))

            cur_layout = QHBoxLayout()
            cur_layout.addWidget(img_label)
            cur_layout.addWidget(cur_label)

            variants_layout.addLayout(cur_layout)

        global_layout.addLayout(variants_layout)
        global_layout.addItem(QSpacerItem(0, 70))

        self.setLayout(global_layout)

        timer = Timer(timer_label)
        timer.start(question['time'], QuestionTestCheckedPage, exam_name, question_number, question, 0)


class WaitingPage(QWidget):
    def __init__(self, exam_name, question_number):
        global timer

        super().__init__(main_window)

        if question_number <= server.number_of_questions(global_group_name, exam_name):
            global_layout = QVBoxLayout()

            question_label = QLabel('Вопрос ' + str(question_number))
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setFont(QFont('Arial', 50))

            global_layout.addWidget(question_label)

            self.setLayout(global_layout)

            question = server.get_question(global_group_name, exam_name, question_number)
            timer = Timer(None)
            if question['type'] == 'Тест':
                timer.start(2, display_page, QuestionTestPage, exam_name, question_number, question)
            elif question['type'] == 'Короткий ответ':
                timer.start(2, display_page, QuestionShortPage, exam_name, question_number, question)
            elif question['type'] == 'Развёрнутый ответ':
                timer.start(2, display_page, QuestionLongPage, exam_name, question_number, question)

        else:
            global_layout = QVBoxLayout()

            exam_finished_label = QLabel('Экзамен завершён!')
            exam_finished_label.setAlignment(Qt.AlignCenter)
            exam_finished_label.setFont(QFont('Arial', 50))

            global_layout.addWidget(exam_finished_label)

            self.setLayout(global_layout)

            timer = Timer(None)
            timer.start(3, display_page, SummaryPage, exam_name)


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
            img_label = QLabel()
            img_label.setPixmap(QPixmap('data\\exam-30x30.png'))
            img_label.setFixedSize(QSize(30, 30))

            cur_label = QLabelClick(exam_name)
            cur_label.setFont(QFont('Arial', 20))
            cur_label.setWordWrap(True)
            cur_label.clicked.connect(return_lambda(display_page, WaitingPage, exam_name, 1))

            cur_layout = QHBoxLayout()
            cur_layout.addWidget(img_label)
            cur_layout.addWidget(cur_label)

            scroll_layout.addLayout(cur_layout)
            scroll_layout.addItem(QSpacerItem(0, 10))

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setFrameShape(QFrame.NoFrame)

        global_layout.addWidget(scroll_area)
        global_layout.addItem(QSpacerItem(0, 20))

        user_label = QLabel('Вы зашли как ' + global_user_name)
        user_label.setFont(QFont('Arial', 15))

        exit_label = QLabelClick('Выход')
        exit_label.setFont(QFont('Arial', 15))

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(user_label)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(exit_label)

        global_layout.addLayout(bottom_layout)

        self.setLayout(global_layout)

        exit_label.clicked.connect(lambda: logout())


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
    encoding = 'utf-8-sig'
    green_color = '#6FCB36'
    red_color = '#F10608'
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
