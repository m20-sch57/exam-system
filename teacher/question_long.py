"""
Widget to edit the long question.
"""


from PyQt5 import Qt
from exam_widget_base import ExamWidgetBase
import common


class QuestionLongEdit(ExamWidgetBase):
    """
    Widget to edit the long question.
    """
    def __init__(self, parent, save_function):
        super().__init__(parent)
        question_data = self.exam_data[self.question - 1]

        statement_title = Qt.QLabel('Текст вопроса ' + str(self.question) + ':')
        statement_title.setFont(Qt.QFont('Arial', 25))

        statement_input = Qt.QPlainTextEdit(question_data['statement'])
        statement_input.setFont(Qt.QFont('Arial', 20))
        statement_input.setMinimumHeight(220)

        maxscore_title = Qt.QLabel('Максимальный балл:')
        maxscore_title.setFont(Qt.QFont('Arial', 25))

        maxscore_input = Qt.QLineEdit(str(question_data['maxscore']))
        maxscore_input.setFont(Qt.QFont('Arial', 20))

        save_button = Qt.QPushButton(Qt.QIcon(common.SAVE), 'Сохранить')
        save_button.setIconSize(Qt.QSize(40, 40))
        save_button.setFont(Qt.QFont('Arial', 20))
        save_button.clicked.connect(lambda: save_function(
            self.exam, self.question,
            {
                'type': question_data['type'],
                'statement': statement_input.toPlainText(),
                'maxscore': maxscore_input.text()
            }
        ))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))

        delete_button = Qt.QPushButton(Qt.QIcon(common.DELETE), 'Удалить')
        delete_button.setIconSize(Qt.QSize(40, 40))
        delete_button.setFont(Qt.QFont('Arial', 20))

        title_layout = Qt.QVBoxLayout()
        title_layout.addWidget(maxscore_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))

        input_layout = Qt.QVBoxLayout()
        input_layout.addWidget(maxscore_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))

        main_layout = Qt.QHBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)

        self.lower_layout.addWidget(save_button)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addWidget(self.status_label)
        self.lower_layout.addStretch(1)
        self.lower_layout.addWidget(delete_button)

        self.layout.addWidget(statement_title)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        self.layout.addWidget(statement_input)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        self.layout.addLayout(main_layout)

    def set_succeeded_state(self):
        """
        Sets succeeded state after saving.
        """
        self.status_label.setText('Сохранено')
        self.status_label.setStyleSheet('color: ' + common.GREEN)
