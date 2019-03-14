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
    def __init__(self, app, question_data):
        super().__init__()
        self.question_data = question_data

        statement_title = Qt.QLabel('Текст вопроса:')
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
        self.save_button.clicked.connect(lambda: app.save_question_data(
            {
                'rowid': self.question_data['rowid'],
                'type': self.question_data['type'],
                'statement': self.statement_input.toPlainText(),
                'correct': '',
                'maxsubs': 1000,
                'maxscore': int(self.maxscore_input.text())
            }
        ))

        self.status_img = Qt.QLabel()
        self.status_img.setScaledContents(True)
        self.status_img.setFixedSize(Qt.QSize(50, 50))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.update_saved_status()

        delete_button = Qt.QPushButton(Qt.QIcon(common.DELETE), 'Удалить')
        delete_button.setIconSize(Qt.QSize(40, 40))
        delete_button.setFont(Qt.QFont('Arial', 20))
        delete_button.clicked.connect(lambda: app.delete_question(self.question_data['rowid']))

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
        self.lower_layout.addWidget(self.status_img)
        self.lower_layout.addWidget(self.status_label)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
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
        saved_maxscore = str(self.question_data['maxscore'])
        if saved_statement != statement or saved_maxscore != maxscore:
            self.status_img.setPixmap(Qt.QPixmap(common.WARNING))
            self.status_label.setText('Сохраните')
            self.status_label.setStyleSheet('color: ' + common.YELLOW)
        else:
            self.status_img.setPixmap(Qt.QPixmap(common.TICK))
            self.status_label.setText('Сохранено')
            self.status_label.setStyleSheet('color: ' + common.GREEN)
        if saved_maxscore != maxscore:
            self.maxscore_input.setStyleSheet('border-color: ' + common.YELLOW)
        else:
            self.maxscore_input.setStyleSheet('border-color: ' + common.GREEN)
        if len(maxscore) > 9 or not maxscore.isdigit():
            self.maxscore_input.setStyleSheet('border-color: ' + common.RED)
            self.status_img.setPixmap(Qt.QPixmap(common.CROSS))
            self.status_label.setText('Недопустимо')
            self.status_label.setStyleSheet('color: ' + common.RED)
            self.save_button.setDisabled(True)
        else:
            self.save_button.setEnabled(True)
