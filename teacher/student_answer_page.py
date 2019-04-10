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
        question_details = common.get_question_details(question_result)

        back_button = Qt.QPushButton(Qt.QIcon(common.LEFT), '', self)
        back_button.setObjectName('Flat')
        back_button.setCursor(Qt.Qt.PointingHandCursor)
        back_button.setIconSize(Qt.QSize(35, 35))
        back_button.clicked.connect(lambda: app.display_results_page(exam_id))

        check_title = Qt.QLabel('Результаты проверки', self)
        check_title.setFont(Qt.QFont('Arial', 30))

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        statement_title = Qt.QLabel('Текст вопроса:', self)
        statement_title.setFont(Qt.QFont('Arial', 25))

        statement_label = Qt.QLabel(question_data['statement'], self)
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_title = Qt.QLabel('Ответ участника:', self)
        answer_title.setFont(Qt.QFont('Arial', 25))

        answer_label = Qt.QLabel(question_details['answer'], self)
        answer_label.setFont(Qt.QFont('Arial', 20))
        answer_label.setWordWrap(True)

        score_title = Qt.QLabel('Получено баллов:', self)
        score_title.setFont(Qt.QFont('Arial', 25))

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addStretch(1)
        upper_layout.addWidget(check_title)
        upper_layout.addStretch(1)

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.addWidget(statement_title)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addWidget(statement_label)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        scroll_layout.addWidget(answer_title)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addWidget(answer_label)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        scroll_layout.addWidget(score_title)
        scroll_layout.addStretch(1)

        scroll_widget = Qt.QWidget(self)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(scroll_area)
        self.setLayout(layout)
