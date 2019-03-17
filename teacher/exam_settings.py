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
    def __init__(self, app, exam_data):
        super().__init__()
        self.exam_data = exam_data

        settings_title = Qt.QLabel('Настройки экзамена')
        settings_title.setFont(Qt.QFont('Arial', 30))

        name_title = Qt.QLabel('Название экзамена:')
        name_title.setFont(Qt.QFont('Arial', 20))

        self.name_input = Qt.QLineEdit(self.exam_data['name'])
        self.name_input.setFont(Qt.QFont('Arial', 20))
        self.name_input.setCursorPosition(0)
        self.name_input.textChanged.connect(self.update_saved_status)

        duration_title = Qt.QLabel('Продолжительность (в минутах):')
        duration_title.setFont(Qt.QFont('Arial', 20))

        self.duration_input = Qt.QLineEdit(str(self.exam_data['duration']))
        self.duration_input.setFont(Qt.QFont('Arial', 20))
        self.duration_input.textChanged.connect(self.update_saved_status)

        state_title = Qt.QLabel('Для участия:')
        state_title.setFont(Qt.QFont('Arial', 20))

        self.state_box = Qt.QComboBox()
        self.state_box.setFont(Qt.QFont('Arial', 20))
        self.state_box.addItems(['Недоступен', 'Открыт'])
        self.state_box.setCurrentIndex(self.exam_data['published'])
        self.state_box.currentIndexChanged.connect(self.update_saved_status)

        self.save_button = Qt.QPushButton(Qt.QIcon(common.SAVE), 'Сохранить')
        self.save_button.setObjectName('Button')
        self.save_button.setIconSize(Qt.QSize(35, 35))
        self.save_button.setFont(Qt.QFont('Arial', 20))
        self.save_button.clicked.connect(lambda: app.save_exam_data(
            {
                'rowid': self.exam_data['rowid'],
                'name': self.name_input.text(),
                'duration': self.duration_input.text(),
                'published': self.state_box.currentIndex()
            }
        ))

        self.status_img = Qt.QLabel()
        self.status_img.setScaledContents(True)
        self.status_img.setFixedSize(Qt.QSize(50, 50))

        self.status_label = Qt.QLabel()
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.update_saved_status()

        delete_button = Qt.QPushButton(Qt.QIcon(common.DELETE), 'Удалить экзамен')
        delete_button.setObjectName('Button')
        delete_button.setIconSize(Qt.QSize(35, 35))
        delete_button.setFont(Qt.QFont('Arial', 20))
        delete_button.clicked.connect(lambda: app.display_confirm_page(
            'Вы уверены, что хотите удалить этот экзамен?',
            lambda: app.display_exam(self.exam_data['rowid']),
            lambda: app.delete_exam(self.exam_data['rowid'])))

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

        self.lower_layout.addWidget(self.save_button)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        self.lower_layout.addWidget(self.status_img)
        self.lower_layout.addWidget(self.status_label)
        self.lower_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
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
        saved_name = self.exam_data['name']
        saved_duration = str(self.exam_data['duration'])
        saved_state = self.exam_data['published']
        if saved_name != name or saved_duration != duration or saved_state != state:
            self.status_img.setPixmap(Qt.QPixmap(common.WARNING))
            self.status_label.setText('Сохраните')
            self.status_label.setStyleSheet('color: ' + common.YELLOW)
        else:
            self.status_img.setPixmap(Qt.QPixmap(common.TICK))
            self.status_label.setText('Сохранено')
            self.status_label.setStyleSheet('color: ' + common.GREEN)
        if saved_name != name:
            self.name_input.setStyleSheet('border-color: ' + common.YELLOW)
        else:
            self.name_input.setStyleSheet('border-color: ' + common.GREEN)
        if saved_duration != duration:
            self.duration_input.setStyleSheet('border-color: ' + common.YELLOW)
        else:
            self.duration_input.setStyleSheet('border-color: ' + common.GREEN)
        if saved_state != state:
            self.state_box.setStyleSheet('border-color: ' + common.YELLOW)
        else:
            self.state_box.setStyleSheet('border-color: ' + common.GREEN)
        if len(duration) > 9 or not duration.isdigit():
            self.duration_input.setStyleSheet('border-color: ' + common.RED)
            self.status_img.setPixmap(Qt.QPixmap(common.CROSS))
            self.status_label.setText('Недопустимо')
            self.status_label.setStyleSheet('color: ' + common.RED)
            self.save_button.setDisabled(True)
        else:
            self.save_button.setEnabled(True)
