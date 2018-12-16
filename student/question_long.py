"""
Contains all widgets for long question.
"""


from PyQt5 import Qt


class QuestionLong(Qt.QWidget):
    """
    Returns widget for long question.
    """
    def __init__(self, parent, check_function):
        super().__init__()
        question_data = parent.exam_data[parent.question - 1]

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        statement_label = Qt.QLabel(question_data['statement'])
        statement_label.setFont(Qt.QFont('Arial', 20))
        statement_label.setWordWrap(True)

        answer_input = Qt.QPlainTextEdit()
        answer_input.setFont(Qt.QFont('Arial', 20))

        scroll_layout = Qt.QVBoxLayout()
        scroll_layout.addWidget(statement_label)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        scroll_layout.addWidget(answer_input)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)
