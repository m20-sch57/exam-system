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
        self.layout.setContentsMargins(0, 0, 10, 10)
        self.lower_layout = Qt.QHBoxLayout()

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(self.layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        layout.addLayout(self.lower_layout)
        self.setLayout(layout)
