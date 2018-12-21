"""
Contains all widgets for long question.
"""


from PyQt5 import Qt
from mywidgets import Label, Pixmap
import common


class QuestionLong(Qt.QWidget):
    """
    Returns widget for long question.
    """
    def __init__(self, parent, check_function, view_question_function):
        super().__init__()
        question_data = parent.exam_data[parent.question - 1]
        answer = question_data['answer'] if question_data['answer'] is not False else ''

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        statement_label = Qt.QLabel(question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))

        answer_input = Qt.QPlainTextEdit()
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setPlainText(answer)
        answer_input.textChanged.connect(
            lambda: self.update_saved_status(answer, answer_input.toPlainText()))
        if question_data['answer'] is not False:
            self.update_saved_status(answer, answer_input.toPlainText())

        save_button = Qt.QPushButton('Сохранить')
        save_button.setFont(Qt.QFont('Arial', 20))
        save_button.setMinimumSize(Qt.QSize(160, 50))
        save_button.clicked.connect(
            lambda: check_function(parent.exam, parent.question, answer_input.toPlainText()))

        next_label = Label('Далее', normal_color=common.BLUE1, hover_color=common.BLUE1)
        next_label.setFont(Qt.QFont('Arial', 30))
        next_label.connect(lambda: view_question_function(parent.exam, parent.question + 1))

        next_img = Pixmap(normal_pic=Qt.QPixmap(common.RIGHT50),
                          hover_pic=Qt.QPixmap(common.RIGHT50))
        next_img.connect(lambda: view_question_function(parent.exam, parent.question + 1))

        save_layout = Qt.QHBoxLayout()
        save_layout.setSpacing(0)
        save_layout.addWidget(save_button)
        save_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        save_layout.addWidget(self.status_label)
        save_layout.addStretch(1)
        if parent.question < len(parent.exam_data):
            save_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
            save_layout.addWidget(next_label)
            save_layout.addWidget(next_img)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.addWidget(statement_label)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addWidget(answer_input)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addLayout(save_layout)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def update_saved_status(self, saved_answer, current_answer):
        """
        Call if current student's answer has changed.
        """
        if saved_answer == current_answer:
            self.status_label.setText('Изменения сохранены')
            self.status_label.setStyleSheet('color: ' + common.GREEN1)
        else:
            self.status_label.setText('Сохраните изменения')
            self.status_label.setStyleSheet('color: ' + common.RED1)


class QuestionLongDetails(Qt.QWidget):
    """
    Returns widget for details of long question.
    """
    def __init__(self, parent):
        super().__init__()
        question_data = parent.exam_data[parent.question - 1]
        current_answer = question_data['answer'] if question_data['answer'] is not False else ''
        current_score = question_data['score'] if question_data['score'] is not False else '0'
        current_score = current_score if current_score != '-1' else 'Неизв.'
        status = common.get_status(current_score, question_data['maxscore'])

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        statement_label = Qt.QLabel(question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_input = Qt.QPlainTextEdit()
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setPlainText(current_answer)
        answer_input.setDisabled(True)

        score_title = Qt.QLabel('Получено баллов:')
        score_title.setFont(Qt.QFont('Arial', 25))
        score_title.setFixedWidth(270)

        score_label = Qt.QLabel(current_score + ' (' + question_data['maxscore'] + ')')
        score_label.setFont(Qt.QFont('Arial', 20))
        score_label.setStyleSheet('color: ' + status['color'])

        score_layout = Qt.QHBoxLayout()
        score_layout.addWidget(score_title)
        score_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        score_layout.addWidget(score_label)
        score_layout.addStretch(1)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.addWidget(statement_label)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addWidget(answer_input)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addLayout(score_layout)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)
