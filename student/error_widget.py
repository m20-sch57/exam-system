"""
Widget to display data error.
"""


from PyQt5 import Qt


class ErrorWidget(Qt.QWidget):
    """
    Widget to display data error.
    """
    def __init__(self, app):
        super().__init__()

        error_title = Qt.QLabel(
            'Произошла ошибка при чтении данных. Возможно, эти данные удалены или недействительны.',
            self)
        error_title.setFont(Qt.QFont('Arial', 25))
        error_title.setWordWrap(True)

        home_button = Qt.QPushButton('На главную', self)
        home_button.setObjectName('Flat')
        home_button.setCursor(Qt.Qt.PointingHandCursor)
        home_button.setFont(Qt.QFont('Arial', 20))
        home_button.clicked.connect(lambda _: app.display_home_page())

        button_layout = Qt.QHBoxLayout()
        button_layout.addWidget(home_button)
        button_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addWidget(error_title)
        layout.addStretch(1)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_status(self):
        """
        Kostyl.
        """
        pass
