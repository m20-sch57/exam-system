"""
Contains widgets for the exam.
"""


from PyQt5 import Qt
from exam_widget_base import ExamWidgetBase
from mywidgets import FlatButton
import common


class ExamSettings(ExamWidgetBase):
    """
    Settings widget for the exam.
    """
    def __init__(self, parent, save_function):
        super().__init__(parent)

        settings_title = Qt.QLabel('Настройки экзамена')
        settings_title.setFont(Qt.QFont('Arial', 30))

        name_title = Qt.QLabel('Название экзамена:')
        name_title.setFont(Qt.QFont('Arial', 20))

        name_input = Qt.QLineEdit(self.exam)
        name_input.setFont(Qt.QFont('Arial', 20))
        name_input.setCursorPosition(0)

        duration_title = Qt.QLabel('Продолжительность (в минутах):')
        duration_title.setFont(Qt.QFont('Arial', 20))

        duration_input = Qt.QLineEdit(self.exam_info['duration'])
        duration_input.setFont(Qt.QFont('Arial', 20))

        state_title = Qt.QLabel('Для участия:')
        state_title.setFont(Qt.QFont('Arial', 20))

        state_box = Qt.QComboBox()
        state_box.setFont(Qt.QFont('Arial', 20))
        state_box.addItems(['Недоступен', 'Открыт'])
        state_box.setCurrentIndex(int(self.exam_info['published']))

        save_button = Qt.QPushButton('Сохранить')
        save_button.setFont(Qt.QFont('Arial', 20))
        save_button.clicked.connect(lambda: save_function(
            self.exam,
            {
                'duration': duration_input.text(),
                'published': state_box.currentIndex()
            }
        ))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))

        delete_button = FlatButton(Qt.QIcon(common.DELETE), 'Удалить')
        delete_button.setIconSize(Qt.QSize(40, 40))
        delete_button.setFont(Qt.QFont('Arial', 20))

        title_layout = Qt.QVBoxLayout()
        title_layout.addWidget(name_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(duration_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(state_title)

        input_layout = Qt.QVBoxLayout()
        input_layout.addWidget(name_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(duration_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(state_box)

        main_layout = Qt.QHBoxLayout()
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)

        self.lower_layout.addWidget(save_button)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addWidget(self.status_label)
        self.lower_layout.addStretch(1)
        self.lower_layout.addWidget(delete_button)

        self.layout.addWidget(settings_title)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        self.layout.addLayout(main_layout)
        self.layout.addStretch(1)

    def set_succeeded_state(self):
        """
        Sets succeeded state after saving.
        """
        self.status_label.setText('Изменения сохранены')
        self.status_label.setStyleSheet('color: ' + common.GREEN)


class QuestionError(Qt.QWidget):
    """
    Widget to display missing question.
    """
    def __init__(self):
        super().__init__()

        error_title = Qt.QLabel('Похоже, этого вопроса уже не существует...')
        error_title.setFont(Qt.QFont('Arial', 25))
        error_title.setWordWrap(True)

        layout = Qt.QVBoxLayout()
        layout.addWidget(error_title)
        layout.addStretch(1)
        self.setLayout(layout)


class QuestionUndefined(Qt.QWidget):
    """
    Widget to display question with undefined type (after creating).
    """
    def __init__(self, parent, create_function):
        super().__init__()
        name_list = [
            'Вопрос с коротким ответом',
            'Вопрос с развёрнутым ответом'
        ]
        type_list = ['Short', 'Long']

        create_title = Qt.QLabel('Создать вопрос')
        create_title.setFont(Qt.QFont('Arial', 30))

        type_title = Qt.QLabel('Тип вопроса:')
        type_title.setFont(Qt.QFont('Arial', 20))

        type_box = Qt.QComboBox()
        type_box.setFont(Qt.QFont('Arial', 20))
        type_box.addItems(name_list)

        create_button = Qt.QPushButton(Qt.QIcon(common.CREATE), 'Создать вопрос')
        create_button.setIconSize(Qt.QSize(40, 40))
        create_button.setFont(Qt.QFont('Arial', 20))
        create_button.clicked.connect(lambda: create_function(
            parent.exam, parent.question, type_list[type_box.currentIndex()]))

        type_layout = Qt.QHBoxLayout()
        type_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        type_layout.addWidget(type_title)
        type_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        type_layout.addWidget(type_box)
        type_layout.addStretch(1)

        button_layout = Qt.QHBoxLayout()
        button_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        button_layout.addWidget(create_button)
        button_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addWidget(create_title)
        layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        layout.addLayout(type_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)


class QuestionShortEdit(ExamWidgetBase):
    """
    Widget to edit the short question.
    """
    def __init__(self, parent, save_function):
        super().__init__(parent)
        question_data = self.exam_data[self.question - 1]

        statement_title = Qt.QLabel('Текст вопроса ' + str(self.question) + ':')
        statement_title.setFont(Qt.QFont('Arial', 25))

        statement_input = Qt.QPlainTextEdit(question_data['statement'])
        statement_input.setFont(Qt.QFont('Arial', 20))
        statement_input.setMinimumHeight(220)

        answer_title = Qt.QLabel('Правильный ответ:')
        answer_title.setFont(Qt.QFont('Arial', 25))

        answer_input = Qt.QLineEdit(question_data['correct'].replace('\n', '; '))
        answer_input.setFont(Qt.QFont('Arial', 20))
        answer_input.setCursorPosition(0)

        maxscore_title = Qt.QLabel('Максимальный балл:')
        maxscore_title.setFont(Qt.QFont('Arial', 25))

        maxscore_input = Qt.QLineEdit(str(question_data['maxscore']))
        maxscore_input.setFont(Qt.QFont('Arial', 20))

        save_button = Qt.QPushButton('Сохранить')
        save_button.setFont(Qt.QFont('Arial', 20))
        save_button.clicked.connect(lambda: save_function(
            self.exam, self.question,
            {
                'type': question_data['type'],
                'statement': statement_input.toPlainText(),
                'correct': answer_input.text().replace('; ', '\n'),
                'maxscore': maxscore_input.text()
            }
        ))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))

        delete_button = FlatButton(Qt.QIcon(common.DELETE), 'Удалить')
        delete_button.setIconSize(Qt.QSize(40, 40))
        delete_button.setFont(Qt.QFont('Arial', 20))

        title_layout = Qt.QVBoxLayout()
        title_layout.addWidget(answer_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(maxscore_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))

        input_layout = Qt.QVBoxLayout()
        input_layout.addWidget(answer_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
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
        self.status_label.setText('Изменения сохранены')
        self.status_label.setStyleSheet('color: ' + common.GREEN)


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

        save_button = Qt.QPushButton('Сохранить')
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

        delete_button = FlatButton(Qt.QIcon(common.DELETE), 'Удалить')
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
        self.status_label.setText('Изменения сохранены')
        self.status_label.setStyleSheet('color: ' + common.GREEN)
