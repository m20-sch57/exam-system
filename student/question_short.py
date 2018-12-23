"""
Contains all widgets for short question.
"""


from PyQt5 import Qt
import common


class QuestionShort(Qt.QWidget):
    """
    Returns widget for short question.
    """
    def __init__(self, parent, check_function):
        super().__init__()
        question_data = parent.exam_data[parent.question - 1]

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        statement_label = Qt.QLabel(question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = Qt.QLabel('Ответ:')
        answer_title.setFont(Qt.QFont('Arial', 30))

        answer_input = Qt.QLineEdit()
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setMinimumWidth(400)

        check_button = Qt.QPushButton('Проверить')
        check_button.setFont(Qt.QFont('Arial', 20))
        check_button.setMinimumSize(Qt.QSize(170, 50))
        check_button.clicked.connect(
            lambda: check_function(parent.exam, parent.question, answer_input.text()))

        answer_layout = Qt.QHBoxLayout()
        answer_layout.addWidget(answer_title)
        answer_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        answer_layout.addWidget(answer_input)
        answer_layout.addStretch(1)
        answer_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        answer_layout.addWidget(check_button)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.addWidget(statement_label)
        scroll_layout.addStretch(1)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addLayout(answer_layout)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class QuestionShortChecked(Qt.QWidget):
    """
    Returns widget for checked short question.
    """
    def __init__(self, parent, view_question_function):
        super().__init__()
        question_data = parent.exam_data[parent.question - 1]
        status = common.get_status(question_data['score'], question_data['maxscore'])

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        statement_label = Qt.QLabel(question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = Qt.QLabel('Ответ:')
        answer_title.setFont(Qt.QFont('Arial', 30))

        answer_input = Qt.QLineEdit(question_data['answer'])
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setDisabled(True)
        answer_input.setMinimumWidth(400)
        answer_input.setStyleSheet(
            'border-width: 2px;'
            'border-color: ' + status['color'] + ';')

        status_img = Qt.QLabel()
        status_img.setPixmap(status['picture'])

        next_button = Qt.QPushButton('Далее')
        next_button.setFont(Qt.QFont('Arial', 20))
        next_button.setMinimumSize(Qt.QSize(130, 50))
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

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.addWidget(statement_label)
        scroll_layout.addStretch(1)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        scroll_layout.addLayout(answer_layout)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class QuestionShortDetails(Qt.QWidget):
    """
    Returns widget for details of short question.
    """
    def __init__(self, parent):
        super().__init__()
        question_data = parent.exam_data[parent.question - 1]
        current_answer = question_data['answer'] if question_data['answer'] is not False else ''
        correct_answer = question_data['correct'].replace('\n', '; ')
        current_score = question_data['score'] if question_data['score'] is not False else '0'
        status = common.get_status(current_score, question_data['maxscore'])

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        statement_label = Qt.QLabel(question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        score_title = Qt.QLabel('Получено баллов:')
        score_title.setFont(Qt.QFont('Arial', 25))
        score_title.setFixedWidth(300)

        score_label = Qt.QLabel(current_score + ' (' + question_data['maxscore'] + ')')
        score_label.setFont(Qt.QFont('Arial', 20))
        score_label.setStyleSheet('color: ' + status['color'])

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

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.addWidget(statement_label)
        scroll_layout.addStretch(1)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        scroll_layout.addLayout(score_layout)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addLayout(your_answer_layout)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addLayout(correct_answer_layout)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)
