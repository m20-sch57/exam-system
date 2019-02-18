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
        self.question_data = self.exam_data[self.question - 1]

        statement_title = Qt.QLabel('Текст вопроса ' + str(self.question) + ':')
        statement_title.setFont(Qt.QFont('Arial', 25))

        self.statement_input = Qt.QPlainTextEdit(self.question_data['statement'])
        self.statement_input.setFont(Qt.QFont('Arial', 20))
        self.statement_input.setMinimumHeight(220)
        self.statement_input.textChanged.connect(self.update_saved_status)

        maxscore_title = Qt.QLabel('Максимальный балл:')
        maxscore_title.setFont(Qt.QFont('Arial', 25))

        self.maxscore_input = Qt.QLineEdit(str(self.question_data['maxscore']))
        self.maxscore_input.setFont(Qt.QFont('Arial', 20))
        self.maxscore_input.textChanged.connect(self.update_saved_status)

        self.save_button = Qt.QPushButton(Qt.QIcon(common.SAVE), 'Сохранить')
        self.save_button.setIconSize(Qt.QSize(40, 40))
        self.save_button.setFont(Qt.QFont('Arial', 20))
        self.save_button.clicked.connect(lambda: save_function(
            self.exam, self.question,
            {
                'type': self.question_data['type'],
                'statement': self.statement_input.toPlainText(),
                'maxscore': self.maxscore_input.text()
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
        input_layout.addWidget(self.maxscore_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))

        main_layout = Qt.QHBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)

        self.lower_layout.addWidget(self.save_button)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addWidget(self.status_label)
        self.lower_layout.addStretch(1)
        self.lower_layout.addWidget(delete_button)

        self.layout.addWidget(statement_title)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        self.layout.addWidget(self.statement_input)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        self.layout.addLayout(main_layout)

    def update_saved_status(self):
        """
        Call after modifying.
        """
        statement = self.statement_input.toPlainText()
        maxscore = self.maxscore_input.text()
        saved_statement = self.question_data['statement']
        saved_maxscore = self.question_data['maxscore']
        if not maxscore.isdigit():
            self.maxscore_input.setStyleSheet('border-color: ' + common.RED)
            self.status_label.setText('Должно быть числом')
            self.status_label.setStyleSheet('color: ' + common.RED)
            self.save_button.setDisabled(True)
            return
        else:
            self.maxscore_input.setStyleSheet('border-color: ' + common.GREEN)
            self.save_button.setEnabled(True)
        if saved_statement == statement and saved_maxscore == maxscore:
            self.status_label.setText('Изменения сохранены')
            self.status_label.setStyleSheet('color: ' + common.GREEN)
        else:
            self.status_label.setText('Сохраните изменения')
            self.status_label.setStyleSheet('color: ' + common.RED)
