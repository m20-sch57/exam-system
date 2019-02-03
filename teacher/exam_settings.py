"""
Contains settings widget for the exam.
"""


from PyQt5 import Qt
from exam_widget_base import ExamWidgetBase


class ExamSettings(ExamWidgetBase):
    """
    Settings widget for the exam.
    """
    def __init__(self, parent):
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

        title_layout = Qt.QVBoxLayout()
        title_layout.addWidget(name_title)
        title_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        title_layout.addWidget(duration_title)

        input_layout = Qt.QVBoxLayout()
        input_layout.addWidget(name_input)
        input_layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        input_layout.addWidget(duration_input)

        main_layout = Qt.QHBoxLayout()
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)

        self.layout.addWidget(settings_title)
        self.layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        self.layout.addLayout(main_layout)
        self.layout.addStretch(1)
        