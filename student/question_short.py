"""
Contains all widgets for short question.
"""


from PyQt5 import Qt
from question_base import QuestionBase
import common


class QuestionShort(QuestionBase):
    """
    Returns widget for short question.
    """
    def __init__(self, app, parent):
        super().__init__(parent)
        question_data = parent.question_data

        statement_label = Qt.QLabel(question_data['statement'], self)
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = Qt.QLabel('Ответ:', self)
        answer_title.setFont(Qt.QFont('Arial', 30))

        answer_input = Qt.QLineEdit(self)
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setMinimumWidth(500)
        answer_input.returnPressed.connect(
            lambda: app.send_submission(question_data['rowid'], answer_input.text()))
        answer_input.setFocus()

        check_button = Qt.QPushButton('Проверить', self)
        check_button.setObjectName('Button')
        check_button.setFont(Qt.QFont('Arial', 20))
        check_button.clicked.connect(
            lambda: app.send_submission(question_data['rowid'], answer_input.text()))

        self.lower_layout.addWidget(answer_title)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addWidget(answer_input)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addStretch(1)
        self.lower_layout.addWidget(check_button)

        self.layout.addWidget(statement_label)
        self.layout.addStretch(1)


class QuestionShortChecked(QuestionBase):
    """
    Returns widget for checked short question.
    """
    def __init__(self, app, parent):
        super().__init__(parent)
        question_data = parent.question_data
        question_result = parent.question_result
        question_style = common.main_question_style(question_result)
        next_question_id = None
        if parent.question_number < len(parent.questions_ids):
            next_question_id = parent.questions_ids[parent.question_number]

        statement_label = Qt.QLabel(question_data['statement'], self)
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = Qt.QLabel('Ответ:', self)
        answer_title.setFont(Qt.QFont('Arial', 30))

        answer_input = Qt.QLineEdit(question_result['answer'], self)
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setMinimumWidth(500)
        answer_input.setDisabled(True)
        answer_input.setStyleSheet(
            'border-width: 2px;'
            'border-color: ' + question_style['main_color'] + ';'
        )

        status_img = Qt.QLabel(self)
        status_img.setScaledContents(True)
        status_img.setPixmap(question_style['main_picture'])
        status_img.setFixedSize(Qt.QSize(50, 50))

        next_button = Qt.QPushButton('Далее', self)
        next_button.setObjectName('Button')
        next_button.setFont(Qt.QFont('Arial', 20))
        next_button.setAutoDefault(True)
        next_button.clicked.connect(lambda: app.view_exam_question(next_question_id))
        next_button.setFocus()
        if next_question_id is None:
            next_button.setDisabled(True)

        self.lower_layout.addWidget(answer_title)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addWidget(answer_input)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        self.lower_layout.addWidget(status_img)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        self.lower_layout.addStretch(1)
        self.lower_layout.addWidget(next_button)

        self.layout.addWidget(statement_label)
        self.layout.addStretch(1)


class QuestionShortDetails(QuestionBase):
    """
    Returns widget for details of short question.
    """
    def __init__(self, parent):
        super().__init__(parent)
        question_data = parent.question_data
        question_result = parent.question_result
        question_details = common.get_question_details(question_result)
        question_style = common.main_question_style(question_result)
        correct_answer = question_data['correct']

        statement_label = Qt.QLabel(question_data['statement'], self)
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        score_title = Qt.QLabel('Получено баллов:', self)
        score_title.setFont(Qt.QFont('Arial', 25))

        score_label = Qt.QLabel(question_details['score'] + ' (' +
                                str(question_data['maxscore']) + ')', self)
        score_label.setFont(Qt.QFont('Arial', 20))
        score_label.setStyleSheet('color: ' + question_style['main_color'])

        your_answer_title = Qt.QLabel('Ваш ответ:', self)
        your_answer_title.setFont(Qt.QFont('Arial', 25))

        your_answer_label = Qt.QLabel(question_details['answer'], self)
        your_answer_label.setFont(Qt.QFont('Arial', 20))

        correct_answer_title = Qt.QLabel('Правильный ответ:', self)
        correct_answer_title.setFont(Qt.QFont('Arial', 25))

        correct_answer_label = Qt.QLabel(correct_answer, self)
        correct_answer_label.setFont(Qt.QFont('Arial', 20))

        title_layout = Qt.QVBoxLayout()
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(score_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(your_answer_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(correct_answer_title)

        value_layout = Qt.QVBoxLayout()
        value_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        value_layout.addWidget(score_label)
        value_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        value_layout.addWidget(your_answer_label)
        value_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        value_layout.addWidget(correct_answer_label)

        main_layout = Qt.QHBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(value_layout)
        main_layout.addStretch(1)

        self.layout.addWidget(statement_label)
        self.layout.addStretch(1)
        self.layout.addLayout(main_layout)
