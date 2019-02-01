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
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setMinimumWidth(450)

        check_button = Qt.QPushButton('Проверить')
        check_button.setFont(Qt.QFont('Arial', 20))
        check_button.clicked.connect(
            lambda: check_function(parent.exam, parent.question, answer_input.text()))

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
    def __init__(self, parent, view_question_function):
        super().__init__(parent)
        question_style = common.main_question_style(self.question_data)

        statement_label = Qt.QLabel(self.question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = Qt.QLabel('Ответ:')
        answer_title.setFont(Qt.QFont('Arial', 30))

        answer_input = Qt.QLineEdit(self.question_data['answer'])
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setMinimumWidth(450)
        answer_input.setDisabled(True)
        answer_input.setStyleSheet(
            'border-width: 2px;'
            'border-color: ' + question_style['main_color'] + ';'
        )

        status_img = Qt.QLabel()
        status_img.setScaledContents(True)
        status_img.setPixmap(question_style['main_picture'])
        status_img.setFixedSize(Qt.QSize(50, 50))

        next_button = Qt.QPushButton('Далее')
        next_button.setFont(Qt.QFont('Arial', 20))
        next_button.clicked.connect(
            lambda: view_question_function(parent.exam, parent.question + 1))

        self.lower_layout.addWidget(answer_title)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addWidget(answer_input)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        self.lower_layout.addWidget(status_img)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        self.lower_layout.addStretch(1)
        if parent.question < len(parent.exam_data):
            self.lower_layout.addWidget(next_button)

        self.layout.addWidget(statement_label)
        self.layout.addStretch(1)


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
        question_style = common.main_question_style(self.question_data)

        statement_label = Qt.QLabel(self.question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        score_title = Qt.QLabel('Получено баллов:')
        score_title.setFont(Qt.QFont('Arial', 25))

        score_label = Qt.QLabel(current_score + ' (' + self.question_data['maxscore'] + ')')
        score_label.setFont(Qt.QFont('Arial', 20))
        score_label.setStyleSheet('color: ' + question_style['main_color'])

        your_answer_title = Qt.QLabel('Ваш ответ:')
        your_answer_title.setFont(Qt.QFont('Arial', 25))

        your_answer_label = Qt.QLabel(current_answer)
        your_answer_label.setFont(Qt.QFont('Arial', 20))

        correct_answer_title = Qt.QLabel('Правильный ответ:')
        correct_answer_title.setFont(Qt.QFont('Arial', 25))

        correct_answer_label = Qt.QLabel(correct_answer)
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
