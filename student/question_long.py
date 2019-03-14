"""
Contains all widgets for long question.
"""


from PyQt5 import Qt
from question_base import QuestionBase
import common


class QuestionLong(QuestionBase):
    """
    Returns widget for long question.
    """
    def __init__(self, app, question_data, question_result, next_question_id):
        super().__init__()
        self.answer = question_result['answer'] if question_result else ''

        statement_label = Qt.QLabel(question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        self.answer_input = Qt.QPlainTextEdit()
        self.answer_input.setFont(Qt.QFont('Arial', 20))
        self.answer_input.setPlainText(self.answer)
        self.answer_input.textChanged.connect(self.update_saved_status)

        save_button = Qt.QPushButton('Сохранить')
        save_button.setFont(Qt.QFont('Arial', 20))
        save_button.clicked.connect(
            lambda: app.send_submission(question_data['rowid'], self.answer_input.toPlainText()))

        self.status_img = Qt.QLabel()
        self.status_img.setScaledContents(True)
        self.status_img.setFixedSize(Qt.QSize(50, 50))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.update_saved_status()

        next_button = Qt.QPushButton('Далее')
        next_button.setFont(Qt.QFont('Arial', 20))
        next_button.clicked.connect(lambda: app.view_exam_question(next_question_id))

        self.lower_layout.addWidget(save_button)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addWidget(self.status_img)
        self.lower_layout.addWidget(self.status_label)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        self.lower_layout.addStretch(1)
        if next_question_id != -1:
            self.lower_layout.addWidget(next_button)

        self.layout.addWidget(statement_label)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        self.layout.addWidget(self.answer_input)

    def update_saved_status(self):
        """
        Call after modifying.
        """
        answer = self.answer
        saved_answer = self.answer_input.toPlainText()
        if saved_answer != answer:
            self.status_img.setPixmap(Qt.QPixmap(common.WARNING))
            self.status_label.setText('Сохраните')
            self.status_label.setStyleSheet('color: ' + common.YELLOW)
        else:
            self.status_img.setPixmap(Qt.QPixmap(common.TICK))
            self.status_label.setText('Сохранено')
            self.status_label.setStyleSheet('color: ' + common.GREEN)


class QuestionLongDetails(QuestionBase):
    """
    Returns widget for details of long question.
    """
    def __init__(self, question_data, question_result):
        super().__init__()
        question_details = common.get_question_details(question_data, question_result)
        question_style = common.main_question_style(question_result)

        statement_label = Qt.QLabel(question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_input = Qt.QPlainTextEdit(question_details['answer'])
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setReadOnly(True)

        score_title = Qt.QLabel('Получено баллов:')
        score_title.setFont(Qt.QFont('Arial', 25))

        score_label = Qt.QLabel(question_details['score'] + ' (' +
                                str(question_data['maxscore']) + ')')
        score_label.setFont(Qt.QFont('Arial', 20))
        score_label.setStyleSheet('color: ' + question_style['main_color'])

        title_layout = Qt.QVBoxLayout()
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(score_title)

        value_layout = Qt.QVBoxLayout()
        value_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        value_layout.addWidget(score_label)

        main_layout = Qt.QHBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(value_layout)
        main_layout.addStretch(1)

        self.layout.addWidget(statement_label)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        self.layout.addWidget(answer_input)
        self.layout.addLayout(main_layout)
