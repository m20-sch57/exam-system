"""
Page to create new group.
"""


from PyQt5 import Qt
import common


class NewGroupPage(Qt.QWidget):
    """
    Page to create new group.
    """
    def __init__(self, app):
        super().__init__()

        back_button = Qt.QPushButton(Qt.QIcon(common.LEFT), '', self)
        back_button.setObjectName('Flat')
        back_button.setCursor(Qt.Qt.PointingHandCursor)
        back_button.setIconSize(Qt.QSize(35, 35))
        back_button.setFixedSize(Qt.QSize(55, 55))
        back_button.clicked.connect(app.display_register_page)

        new_group_title = Qt.QLabel('Новая группа', self)
        new_group_title.setFont(Qt.QFont('Arial', 30))

        group_title = Qt.QLabel('Название группы:', self)
        group_title.setFont(Qt.QFont('Arial', 20))

        group_input = Qt.QLineEdit(self)
        group_input.setFont(Qt.QFont('Arial', 20))
        group_input.setMinimumWidth(400)

        create_button = Qt.QPushButton(Qt.QIcon(common.CREATE), 'Создать группу', self)
        create_button.setObjectName('Button')
        create_button.setIconSize(Qt.QSize(35, 35))
        create_button.setFont(Qt.QFont('Arial', 20))
        create_button.clicked.connect(lambda: app.create_group(group_input.text()))
        group_input.returnPressed.connect(create_button.click)

        self.status_label = Qt.QLabel(self)
        self.status_label.setFont(Qt.QFont('Arial', 20))
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumWidth(380)

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addStretch(1)
        upper_layout.addWidget(new_group_title)
        upper_layout.addStretch(1)

        title_layout = Qt.QVBoxLayout()
        title_layout.addWidget(group_title)

        input_layout = Qt.QVBoxLayout()
        input_layout.addWidget(group_input)

        main_layout = Qt.QHBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(title_layout)
        main_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        main_layout.addLayout(input_layout)
        main_layout.addStretch(1)

        button_layout = Qt.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(create_button)
        button_layout.addSpacerItem(Qt.QSpacerItem(20, 0))
        button_layout.addWidget(self.status_label)
        button_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addStretch(1)
        layout.addLayout(main_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 40))
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)

    def set_waiting_state(self):
        """
        Sets waiting state.
        """
        self.setCursor(Qt.Qt.WaitCursor)
        self.status_label.setText('Подождите...')
        self.status_label.setStyleSheet('color: black')
        self.status_label.repaint()

    def set_failed_state(self, status):
        """
        Sets failed state.
        """
        self.setCursor(Qt.Qt.ArrowCursor)
        self.status_label.setText(status)
        self.status_label.setStyleSheet('color: ' + common.RED)
