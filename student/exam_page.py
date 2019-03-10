"""
Exam page for student.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class ExamPage(Qt.QWidget):
    """
    Exam page for student.
    """
    def __init__(self, app, exam_id):
        super().__init__()
        self.app = app
        self.exam_id = exam_id
        self.question_id = None
        self.questions_ids = []
        self.questions_results = []

        back_button = FlatButton(Qt.QIcon(common.LEFT), '')
        back_button.setIconSize(Qt.QSize(40, 40))
        back_button.setFixedSize(back_button.sizeHint())
        back_button.clicked.connect(app.display_home_page)

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

    def display_question(self, exam_data, question_data):
        """
        Displays current question.
        """
        self.question_id = question_data['rowid'] if question_data else -1
        self.refresh()
        old_widget = self.layout().itemAt(3).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        old_widget = self.layout().itemAt(2).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        status_widget = self.app.get_exam_status_widget(self, exam_data)
        self.widget = self.app.get_question_widget(exam_data, question_data)
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
        for question in range(len(self.questions_ids)):
            question_id = self.questions_ids[question]['rowid']
            question_result = self.questions_results[question]
            question_button = Qt.QPushButton(str(question + 1))
            question_button.setCursor(Qt.Qt.PointingHandCursor)
            question_button.setFixedSize(Qt.QSize(50, 50))
            question_button.clicked.connect(
                common.return_lambda(self.app.view_exam_question, question_id))
            question_button.setStyleSheet(
                common.upper_question_style(question_result, question, self.question))
            self.questions_layout.addWidget(question_button)
