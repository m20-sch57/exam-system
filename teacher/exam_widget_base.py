"""
Contains base class for exam widgets.
"""


from PyQt5 import Qt


class ExamWidgetBase(Qt.QWidget):
    """
    Exam widget base class.
    """
    def __init__(self, parent):
        super().__init__()
        self.exam = parent.exam
        self.exam_data = parent.exam_data
        self.exam_info = parent.exam_info
        self.question = parent.question

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)

        self.layout = Qt.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.lower_layout = Qt.QHBoxLayout()

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(self.layout)
        scroll_area.setWidget(scroll_widget)

        layout = Qt.QVBoxLayout()
        layout.addWidget(scroll_area)
        layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        layout.addLayout(self.lower_layout)
        self.setLayout(layout)
