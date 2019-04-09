"""
Page to display student's answer for the question.
"""


from PyQt5 import Qt
from exam_widget_base import ExamWidgetBase
import common


class StudentAnswerPage(ExamWidgetBase):
    """
    Page to display student's answer for the question.
    """
    def __init__(self, app, exam_id, question_id, user_id, question_data, question_result):
        super().__init__()

        back_button = Qt.QPushButton(Qt.QIcon(common.LEFT), '', self)
        back_button.setObjectName('Flat')
        back_button.setCursor(Qt.Qt.PointingHandCursor)
        back_button.setIconSize(Qt.QSize(35, 35))
        back_button.clicked.connect(lambda: app.display_results_page(exam_id))

        check_title = Qt.QLabel('Результаты проверки', self)
        check_title.setFont(Qt.QFont('Arial', 30))

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addStretch(1)
        upper_layout.addWidget(check_title)
        upper_layout.addStretch(1)

        self.layout.addLayout(upper_layout)
        self.layout.addStretch(1)
