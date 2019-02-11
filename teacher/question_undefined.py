"""
Widget to display question with undefined type.
"""


from PyQt5 import Qt
import common


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
