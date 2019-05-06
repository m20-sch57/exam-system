"""
Page to display student's answer for the question.
"""


from PyQt5 import Qt
import common


class StudentAnswerPage(Qt.QWidget):
    """
    Page to display student's answer for the question.
    """
    def __init__(self, app, exam_id, question_data, question_result):
        super().__init__()
        self.question_data = question_data
        self.question_details = common.get_question_details(question_result)

        back_button = Qt.QPushButton(Qt.QIcon(common.LEFT), '', self)
        back_button.setObjectName('Flat')
        back_button.setCursor(Qt.Qt.PointingHandCursor)
        back_button.setIconSize(Qt.QSize(35, 35))
        back_button.setFixedSize(Qt.QSize(55, 55))
        back_button.clicked.connect(lambda: app.display_results_page(exam_id))

        check_title = Qt.QLabel('Результаты проверки', self)
        check_title.setFont(Qt.QFont('Arial', 30))

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        statement_title = Qt.QLabel('Текст вопроса:', self)
        statement_title.setFont(Qt.QFont('Arial', 25))

        statement_label = Qt.QLabel(self.question_data['statement'], self)
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = Qt.QLabel('Ответ участника:', self)
        answer_title.setFont(Qt.QFont('Arial', 25))

        answer_label = Qt.QLabel(self.question_details['answer'], self)
        answer_label.setFont(Qt.QFont('Arial', 20))
        answer_label.setWordWrap(True)

        self.save_button = Qt.QPushButton('Сохранить', self)
        self.save_button.setObjectName('Button')
        self.save_button.setFont(Qt.QFont('Arial', 20))
        self.save_button.clicked.connect(lambda: app.save_submission_score(
            exam_id, self.question_data['rowid'],
            question_result['rowid'], self.score_input.text()
        ))

        score_title = Qt.QLabel('Баллы (из ' + str(self.question_data['maxscore']) + '):', self)
        score_title.setFont(Qt.QFont('Arial', 20))

        self.score_input = Qt.QLineEdit(self.question_details['score'], self)
        self.score_input.setFont(Qt.QFont('Arial', 20))
        self.score_input.setMinimumWidth(200)
        self.score_input.textChanged.connect(self.update_status)
        self.score_input.returnPressed.connect(self.save_button.click)

        self.status_img = Qt.QLabel(self)
        self.status_img.setScaledContents(True)
        self.status_img.setFixedSize(Qt.QSize(50, 50))

        self.status_label = Qt.QLabel(self)
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.update_status()

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addStretch(1)
        upper_layout.addWidget(check_title)
        upper_layout.addStretch(1)

        statement_layout = Qt.QVBoxLayout()
        statement_layout.addWidget(statement_title)
        statement_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        statement_layout.addWidget(statement_label)

        answer_layout = Qt.QVBoxLayout()
        answer_layout.addWidget(answer_title)
        answer_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        answer_layout.addWidget(answer_label)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.addLayout(statement_layout)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        scroll_layout.addLayout(answer_layout)
        scroll_layout.addStretch(1)

        scroll_widget = Qt.QWidget(self)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        score_layout = Qt.QHBoxLayout()
        score_layout.addWidget(score_title)
        score_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        score_layout.addWidget(self.score_input)

        save_layout = Qt.QHBoxLayout()
        save_layout.addWidget(self.save_button)
        save_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        save_layout.addWidget(self.status_img)
        save_layout.addWidget(self.status_label)
        save_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        save_layout.addStretch(1)
        save_layout.addLayout(score_layout)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(scroll_area)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(save_layout)
        self.setLayout(layout)

    def update_status(self):
        """
        Call after modifying.
        """
        score = self.score_input.text()
        saved_score = self.question_details['score']
        maxscore = self.question_data['maxscore']
        if saved_score != score:
            self.status_img.setPixmap(Qt.QPixmap(common.WARNING))
            self.status_label.setText('Сохраните')
            self.status_label.setStyleSheet('color: ' + common.YELLOW)
        else:
            self.status_img.setPixmap(Qt.QPixmap(common.TICK))
            self.status_label.setText('Сохранено')
            self.status_label.setStyleSheet('color: ' + common.GREEN)
        if score != '?' and (not score.isdigit() or not int(score) <= maxscore):
            self.status_img.setPixmap(Qt.QPixmap(common.CROSS))
            self.status_label.setText('Недопустимо')
            self.status_label.setStyleSheet('color: ' + common.RED)
            self.save_button.setDisabled(True)
        else:
            self.save_button.setEnabled(True)
