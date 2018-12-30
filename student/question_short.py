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
    def __init__(self, parent, check_function):
        super().__init__(parent)

        statement_label = Qt.QLabel(self.question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = Qt.QLabel('Ответ:')
        answer_title.setFont(Qt.QFont('Arial', 30))

        answer_input = Qt.QLineEdit()
        answer_input.setMinimumWidth(400)

        check_button = Qt.QPushButton('Проверить')
        check_button.clicked.connect(
            lambda: check_function(parent.exam, parent.question, answer_input.text()))

        answer_layout = Qt.QHBoxLayout()
        answer_layout.addWidget(answer_title)
        answer_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        answer_layout.addWidget(answer_input)
        answer_layout.addStretch(1)
        answer_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        answer_layout.addWidget(check_button)

        self.layout.addWidget(statement_label)
        self.layout.addStretch(1)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        self.layout.addLayout(answer_layout)


class QuestionShortChecked(QuestionBase):
    """
    Returns widget for checked short question.
    """
    def __init__(self, parent, view_question_function):
        super().__init__(parent)
        question_style = common.get_question_style(self.question_data)

        statement_label = Qt.QLabel(self.question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = Qt.QLabel('Ответ:')
        answer_title.setFont(Qt.QFont('Arial', 30))

        answer_input = Qt.QLineEdit(self.question_data['answer'])
        answer_input.setDisabled(True)
        answer_input.setMinimumWidth(400)
        answer_input.setStyleSheet(
            'border-width: 2px;'
            'border-color: ' + question_style['main_color'] + ';'
        )

        status_img = Qt.QLabel()
        status_img.setScaledContents(True)
        status_img.setPixmap(question_style['main_picture'])
        status_img.setFixedSize(Qt.QSize(50, 50))

        next_button = Qt.QPushButton('Далее')
        next_button.clicked.connect(
            lambda: view_question_function(parent.exam, parent.question + 1))

        answer_layout = Qt.QHBoxLayout()
        answer_layout.addWidget(answer_title)
        answer_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        answer_layout.addWidget(answer_input)
        answer_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        answer_layout.addWidget(status_img)
        answer_layout.addStretch(1)
        answer_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        if parent.question < len(parent.exam_data):
            answer_layout.addWidget(next_button)

        self.layout.addWidget(statement_label)
        self.layout.addStretch(1)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        self.layout.addLayout(answer_layout)


class QuestionShortDetails(QuestionBase):
    """
    Returns widget for details of short question.
    """
    def __init__(self, parent):
        super().__init__(parent)
        current_answer = self.question_data['answer']
        if current_answer is False:
            current_answer = ''
        correct_answer = self.question_data['correct'].replace('\n', '; ')
        current_score = self.question_data['score']
        if current_score is False:
            current_score = '0'
        question_style = common.get_question_style(self.question_data)

        statement_label = Qt.QLabel(self.question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        score_title = Qt.QLabel('Получено баллов:')
        score_title.setFont(Qt.QFont('Arial', 25))
        score_title.setFixedWidth(300)

        score_label = Qt.QLabel(current_score + ' (' + self.question_data['maxscore'] + ')')
        score_label.setFont(Qt.QFont('Arial', 20))
        score_label.setStyleSheet('color: ' + question_style['main_color'])

        your_answer_title = Qt.QLabel('Ваш ответ:')
        your_answer_title.setFont(Qt.QFont('Arial', 25))
        your_answer_title.setFixedWidth(300)

        your_answer_label = Qt.QLabel(current_answer)
        your_answer_label.setFont(Qt.QFont('Arial', 20))
        your_answer_label.setWordWrap(True)

        correct_answer_title = Qt.QLabel('Правильный ответ:')
        correct_answer_title.setFont(Qt.QFont('Arial', 25))
        correct_answer_title.setFixedWidth(300)

        correct_answer_label = Qt.QLabel(correct_answer)
        correct_answer_label.setFont(Qt.QFont('Arial', 20))
        correct_answer_label.setWordWrap(True)

        score_layout = Qt.QHBoxLayout()
        score_layout.addWidget(score_title)
        score_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        score_layout.addWidget(score_label)
        score_layout.addStretch(1)

        your_answer_layout = Qt.QHBoxLayout()
        your_answer_layout.addWidget(your_answer_title)
        your_answer_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        your_answer_layout.addWidget(your_answer_label)

        correct_answer_layout = Qt.QHBoxLayout()
        correct_answer_layout.addWidget(correct_answer_title)
        correct_answer_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        correct_answer_layout.addWidget(correct_answer_label)

        self.layout.addWidget(statement_label)
        self.layout.addStretch(1)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        self.layout.addLayout(score_layout)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        self.layout.addLayout(your_answer_layout)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        self.layout.addLayout(correct_answer_layout)
