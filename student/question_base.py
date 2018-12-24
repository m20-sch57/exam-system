"""
Contains base class for question widgets.
"""


from PyQt5 import Qt


class QuestionBase(Qt.QWidget):
    """
    Question basic class.
    """
    def __init__(self, parent):
        super().__init__()
        self.question_data = parent.exam_data[parent.question - 1]

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        self.layout = Qt.QVBoxLayout()

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(self.layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)
