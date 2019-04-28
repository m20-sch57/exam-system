"""
Widget to display data error.
"""


from PyQt5 import Qt


class ErrorWidget(Qt.QWidget):
    """
    Widget to display data error.
    """
    def __init__(self):
        super().__init__()

        error_title = Qt.QLabel(
            'Произошла ошибка при чтении данных. Возможно, эти данные удалены или недействительны.',
            self)
        error_title.setFont(Qt.QFont('Arial', 25))
        error_title.setWordWrap(True)

        layout = Qt.QVBoxLayout()
        layout.addWidget(error_title)
        layout.addStretch(1)
        self.setLayout(layout)

    def update_status(self):
        """
        Kostyl.
        """
        pass
