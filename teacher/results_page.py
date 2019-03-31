"""
Page to display the results table of the exam.
"""


from PyQt5 import Qt
import common


class ResultsPage(Qt.QWidget):
    """
    Page to display the results table of the exam.
    """
    def __init__(self, app, exam_id, users, questions_ids, results_table):
        super().__init__()

        back_button = Qt.QPushButton(Qt.QIcon(common.LEFT), '', self)
        back_button.setObjectName('Flat')
        back_button.setCursor(Qt.Qt.PointingHandCursor)
        back_button.setIconSize(Qt.QSize(35, 35))
        back_button.clicked.connect(lambda: app.display_exam(exam_id))

        results_title = Qt.QLabel('Таблица результатов', self)
        results_title.setFont(Qt.QFont('Arial', 30))

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addWidget(back_button)
        upper_layout.addStretch(1)
        upper_layout.addWidget(results_title)
        upper_layout.addStretch(1)

        layout = Qt.QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addStretch(1)
        self.setLayout(layout)
