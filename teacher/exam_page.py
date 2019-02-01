"""
Exam page for teacher.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class ExamPage(Qt.QWidget):
    """
    Exam page for teacher.
    """
    def __init__(self, exam, back_function, view_question_function,
                 settings_function, create_function,
                 get_settings_function, get_question_function):
        super().__init__()
        self.exam = exam
        self.question = None
        self.exam_data = None
        self.exam_info = None
        self.view_question_function = view_question_function
        self.settings_function = settings_function
        self.create_function = create_function
        self.get_settings_function = get_settings_function
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

        self.settings_button = FlatButton(Qt.QIcon(common.SETTINGS), '')
        self.settings_button.setCursor(Qt.Qt.PointingHandCursor)
        self.settings_button.setFixedSize(Qt.QSize(50, 50))
        self.settings_button.setIconSize(Qt.QSize(30, 30))
        self.settings_button.clicked.connect(lambda _: self.settings_function(self.exam))

        self.questions_layout = Qt.QHBoxLayout()
        self.questions_layout.setSpacing(0)

        create_button = FlatButton(Qt.QIcon(common.CREATE), '')
        create_button.setCursor(Qt.Qt.PointingHandCursor)
        create_button.setFixedSize(Qt.QSize(50, 50))
        create_button.setIconSize(Qt.QSize(40, 40))

        scroll_layout = Qt.QHBoxLayout()
        scroll_layout.setSpacing(0)
        scroll_layout.setSizeConstraint(Qt.QLayout.SetMinimumSize)
        scroll_layout.addWidget(self.settings_button)
        scroll_layout.addLayout(self.questions_layout)
        scroll_layout.addSpacerItem(Qt.QSpacerItem(5, 0))
        scroll_layout.addWidget(create_button)
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
        self.setLayout(layout)

    def display_question(self, question, exam_data, exam_info):
        """
        Displays current question.
        """
        self.question = question
        self.exam_data = exam_data
        self.exam_info = exam_info
        self.refresh()

        question_widget = self.get_question_function(self)
        old_widget = self.layout().itemAt(2).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        self.layout().addWidget(question_widget)

    def display_settings(self, exam_data, exam_info):
        """
        Displays exam settings.
        """
        self.question = None
        self.exam_data = exam_data
        self.exam_info = exam_info
        self.refresh()

        settings_widget = self.get_settings_function(self)
        old_widget = self.layout().itemAt(2).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        self.layout().addWidget(settings_widget)

    def refresh(self):
        """
        Refreshes upper panel.
        """
        self.settings_button.setStyleSheet(common.upper_question_style(None, self.question))
        while self.questions_layout.count() > 0:
            old_widget = self.questions_layout.itemAt(0).widget()
            old_widget.deleteLater()
            self.questions_layout.removeWidget(old_widget)
        for question in range(1, len(self.exam_data) + 1):
            question_button = Qt.QPushButton(str(question))
            question_button.setCursor(Qt.Qt.PointingHandCursor)
            question_button.setFixedSize(Qt.QSize(50, 50))
            question_button.clicked.connect(
                common.return_lambda(self.view_question_function, self.exam, question))
            question_button.setStyleSheet(common.upper_question_style(question, self.question))
            self.questions_layout.addWidget(question_button)
