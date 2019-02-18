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
    def __init__(self, parent, check_function, view_question_function):
        super().__init__(parent)

        statement_label = Qt.QLabel(self.question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))

        self.answer_input = Qt.QPlainTextEdit()
        self.answer_input.setFont(Qt.QFont('Arial', 20))
        if self.question_data['answer'] is not False:
            self.answer_input.setPlainText(self.question_data['answer'])
        self.answer_input.textChanged.connect(self.update_saved_status)

        save_button = Qt.QPushButton('Сохранить')
        save_button.setFont(Qt.QFont('Arial', 20))
        save_button.clicked.connect(
            lambda: check_function(parent.exam, parent.question, self.answer_input.toPlainText()))

        next_button = Qt.QPushButton('Далее')
        next_button.setFont(Qt.QFont('Arial', 20))
        next_button.clicked.connect(
            lambda: view_question_function(parent.exam, parent.question + 1))

        self.lower_layout.addWidget(save_button)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addWidget(self.status_label)
        self.lower_layout.addStretch(1)
        if parent.question < len(parent.exam_data):
            self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
            self.lower_layout.addWidget(next_button)

        self.layout.addWidget(statement_label)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        self.layout.addWidget(self.answer_input)

    def update_saved_status(self):
        """
        Call after modifying.
        """
        answer = self.question_data['answer']
        saved_answer = self.answer_input.toPlainText()
        if saved_answer == answer:
            self.status_label.setText('Изменения сохранены')
            self.status_label.setStyleSheet('color: ' + common.GREEN)
        else:
            self.status_label.setText('Сохраните изменения')
            self.status_label.setStyleSheet('color: ' + common.RED)


class QuestionLongDetails(QuestionBase):
    """
    Returns widget for details of long question.
    """
    def __init__(self, parent):
        super().__init__(parent)
        current_answer = self.question_data['answer']
        if current_answer is False:
            current_answer = ''
        current_score = self.question_data['score']
        if current_score is False:
            current_score = '0'
        if current_score == '-1':
            current_score = 'Неизв.'
        question_style = common.main_question_style(self.question_data)

        statement_label = Qt.QLabel(self.question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_input = Qt.QPlainTextEdit(current_answer)
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setReadOnly(True)

        score_title = Qt.QLabel('Получено баллов:')
        score_title.setFont(Qt.QFont('Arial', 25))

        score_label = Qt.QLabel(current_score + ' (' + self.question_data['maxscore'] + ')')
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
