"""
Contains all widgets for short question.
"""


import os
from PyQt5.Qt import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.Qt import QLabel, QLineEdit, QScrollArea
from PyQt5.Qt import QFont, QPixmap, QSize, QSpacerItem, QFrame
from mywidgets import Label, Pixmap


def get_status(score, maxscore):
    """
    Returns color and picture depending on the result.
    """
    if score == maxscore:
        return {'color': '#6FCB36', 'picture': QPixmap(os.path.join('data', 'tick-50x50.png'))}
    else:
        return {'color': '#F10608', 'picture': QPixmap(os.path.join('data', 'cross-50x50.png'))}


class QuestionShortDetails(QWidget):
    """
    Returns widget for details of short question.
    """
    def __init__(self, parent):
        super().__init__()
        question_data = parent.exam_data[parent.question - 1]
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
        score_label.setFont(QFont('Arial', 20))

        your_answer_layout = QHBoxLayout()
        your_answer_layout.addWidget(your_answer_title)
        your_answer_layout.addSpacerItem(QSpacerItem(20, 0))
        your_answer_layout.addWidget(your_answer_label)
        your_answer_layout.addSpacerItem(QSpacerItem(10, 0))
        your_answer_layout.addWidget(status_img)
        your_answer_layout.addStretch(1)

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
    def __init__(self, parent, finish_function, view_question_function):
        super().__init__()
        question_data = parent.exam_data[parent.question - 1]
        status = get_status(int(question_data['score']), int(question_data['maxscore']))
        if parent.question == len(parent.exam_data):
            next_text = 'Закончить'
            next_func = lambda: finish_function(parent.exam)
        else:
            next_text = 'Далее'
            next_func = lambda: view_question_function(parent.exam, parent.question + 1)

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
        next_label.connect(next_func)

        next_img = Pixmap(normal_pic=QPixmap(os.path.join('data', 'right-50x50.png')),
                          hover_pic=QPixmap(os.path.join('data', 'right-50x50.png')))
        next_img.connect(next_func)

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
    def __init__(self, parent, check_function):
        super().__init__()
        question_data = parent.exam_data[parent.question - 1]

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
        check_label.connect(
            lambda: check_function(parent.exam, parent.question, answer_input.text()))

        check_img = Pixmap(normal_pic=QPixmap(os.path.join('data', 'right-50x50.png')),
                           hover_pic=QPixmap(os.path.join('data', 'right-50x50.png')))
        check_img.connect(
            lambda: check_function(parent.exam, parent.question, answer_input.text()))

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
