"""
Page that is displayed when student is passing the exam.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class ExamPage(Qt.QWidget):
    """
    Page that is displayed when student is passing the exam.
    """
    def __init__(self, exam, back_function, view_question_function,
                 get_exam_status_function, get_question_function):
        super().__init__()
        self.exam = exam
        self.question = None
        self.exam_data = None
        self.exam_info = None
        self.view_question_function = view_question_function
        self.get_exam_status_function = get_exam_status_function
        self.get_question_function = get_question_function

        back_button = FlatButton(Qt.QIcon(common.LEFT), '')
        back_button.setIconSize(Qt.QSize(40, 40))
        back_button.setFixedSize(back_button.sizeHint())
        back_button.clicked.connect(lambda _: back_function())

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)
        scroll_area.setMinimumHeight(50 + scroll_area.verticalScrollBar().sizeHint().height())
        scroll_area.setSizePolicy(Qt.QSizePolicy.Minimum, Qt.QSizePolicy.Minimum)

        self.questions_layout = Qt.QHBoxLayout()
        self.questions_layout.setSpacing(0)
        self.widget = Qt.QWidget()

        scroll_layout = Qt.QHBoxLayout()
        scroll_layout.setSizeConstraint(Qt.QLayout.SetMinimumSize)
        scroll_layout.addStretch(1)
        scroll_layout.addLayout(self.questions_layout)
        scroll_layout.addStretch(1)

        scroll_widget = Qt.QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addSpacerItem(Qt.QSpacerItem(10, 0))
        upper_layout.addWidget(scroll_area)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 10))
        layout.addWidget(Qt.QWidget())
        layout.addWidget(self.widget)
        self.setLayout(layout)

    def display(self, question, exam_data, exam_info):
        """
        Displays current question.
        """
        self.question = question
        self.exam_data = exam_data
        self.exam_info = exam_info
        self.refresh()

        old_widget = self.layout().itemAt(3).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        old_widget = self.layout().itemAt(2).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        status_widget = self.get_exam_status_function(self)
        self.widget = self.get_question_function(self)
        self.layout().addWidget(status_widget)
        self.layout().addWidget(self.widget)

    def refresh(self):
        """
        Refreshes upper panel.
        """
        while self.questions_layout.count() > 0:
            old_widget = self.questions_layout.itemAt(0).widget()
            old_widget.deleteLater()
            self.questions_layout.removeWidget(old_widget)
        for question in range(1, len(self.exam_data) + 1):
            question_data = self.exam_data[question - 1]
            question_button = Qt.QPushButton(str(question))
            question_button.setCursor(Qt.Qt.PointingHandCursor)
            question_button.setFixedSize(Qt.QSize(50, 50))
            question_button.clicked.connect(
                common.return_lambda(self.view_question_function, self.exam, question))
            question_button.setStyleSheet(
                common.upper_question_style(question_data, question, self.question))
            self.questions_layout.addWidget(question_button)
