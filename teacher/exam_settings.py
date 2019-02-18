"""
Contains settings widget for the exam.
"""


from PyQt5 import Qt
from exam_widget_base import ExamWidgetBase
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

        self.name_input = Qt.QLineEdit(self.exam)
        self.name_input.setFont(Qt.QFont('Arial', 20))
        self.name_input.setCursorPosition(0)
        self.name_input.textChanged.connect(self.update_saved_status)

        duration_title = Qt.QLabel('Продолжительность (в минутах):')
        duration_title.setFont(Qt.QFont('Arial', 20))

        self.duration_input = Qt.QLineEdit(self.exam_info['duration'])
        self.duration_input.setFont(Qt.QFont('Arial', 20))
        self.duration_input.textChanged.connect(self.update_saved_status)

        state_title = Qt.QLabel('Для участия:')
        state_title.setFont(Qt.QFont('Arial', 20))

        self.state_box = Qt.QComboBox()
        self.state_box.setFont(Qt.QFont('Arial', 20))
        self.state_box.addItems(['Недоступен', 'Открыт'])
        self.state_box.setCurrentIndex(int(self.exam_info['published']))
        self.state_box.currentIndexChanged.connect(self.update_saved_status)

        save_button = Qt.QPushButton(Qt.QIcon(common.SAVE), 'Сохранить')
        save_button.setIconSize(Qt.QSize(40, 40))
        save_button.setFont(Qt.QFont('Arial', 20))
        save_button.clicked.connect(lambda: save_function(
            self.exam,
            {
                'duration': self.duration_input.text(),
                'published': self.state_box.currentIndex()
            }
        ))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))

        delete_button = Qt.QPushButton(Qt.QIcon(common.DELETE), 'Удалить')
        delete_button.setIconSize(Qt.QSize(40, 40))
        delete_button.setFont(Qt.QFont('Arial', 20))

        title_layout = Qt.QVBoxLayout()
        title_layout.addWidget(name_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(duration_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(state_title)

        input_layout = Qt.QVBoxLayout()
        input_layout.addWidget(self.name_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(self.duration_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(self.state_box)

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

    def update_saved_status(self):
        """
        Call after modifying.
        """
        name = self.name_input.text()
        duration = self.duration_input.text()
        state = self.state_box.currentIndex()
        saved_name = self.exam
        saved_duration = self.exam_info['duration']
        saved_state = int(self.exam_info['published'])
        if saved_name == name and saved_duration == duration and saved_state == state:
            self.status_label.setText('Сохранено')
            self.status_label.setStyleSheet('color: ' + common.GREEN)
        else:
            self.status_label.setText('Сохраните')
            self.status_label.setStyleSheet('color: ' + common.RED)
