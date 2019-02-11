"""
Widget to display missing question.
"""


from PyQt5 import Qt


class QuestionError(Qt.QWidget):
    """
    Widget to display missing question.
    """
    def __init__(self):
        super().__init__()

        error_title = Qt.QLabel('Не удалось найти этот вопрос. Возможно, он был удалён.')
        error_title.setFont(Qt.QFont('Arial', 25))
        error_title.setWordWrap(True)

        layout = Qt.QVBoxLayout()
        layout.addWidget(error_title)
        layout.addStretch(1)
        self.setLayout(layout)
