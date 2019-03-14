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
    def __init__(self, app, exam_id):
        super().__init__()
        self.app = app
        self.exam_id = exam_id
        self.question_id = None
        self.questions_ids = []

        back_button = FlatButton(Qt.QIcon(common.LEFT), '')
        back_button.setIconSize(Qt.QSize(40, 40))
        back_button.setFixedSize(back_button.sizeHint())
        back_button.clicked.connect(app.display_home_page)

        scroll_area = Qt.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.QFrame.NoFrame)
        scroll_area.setMinimumHeight(50 + scroll_area.verticalScrollBar().sizeHint().height())
        scroll_area.setSizePolicy(Qt.QSizePolicy.Minimum, Qt.QSizePolicy.Minimum)

        self.settings_button = FlatButton(Qt.QIcon(common.SETTINGS), '')
        self.settings_button.setCursor(Qt.Qt.PointingHandCursor)
        self.settings_button.setFixedSize(Qt.QSize(50, 50))
        self.settings_button.setIconSize(Qt.QSize(30, 30))
        self.settings_button.clicked.connect(lambda _: self.app.view_exam_settings())

        self.questions_layout = Qt.QHBoxLayout()
        self.questions_layout.setSpacing(0)

        short_question_action = Qt.QWidgetAction(self)
        short_question_action.setFont(Qt.QFont('Arial', 15))
        short_question_action.setText('Вопрос SHORT')
        short_question_action.triggered.connect(
            lambda: self.app.create_question(self.exam_id, 'Short'))

        long_question_action = Qt.QWidgetAction(self)
        long_question_action.setFont(Qt.QFont('Arial', 15))
        long_question_action.setText('Вопрос LONG')
        long_question_action.triggered.connect(
            lambda: self.app.create_question(self.exam_id, 'Long'))

        create_menu = Qt.QMenu()
        create_menu.addAction(short_question_action)
        create_menu.addAction(long_question_action)

        create_button = FlatButton(Qt.QIcon(common.CREATE), '')
        create_button.setCursor(Qt.Qt.PointingHandCursor)
        create_button.setFixedSize(Qt.QSize(50, 50))
        create_button.setIconSize(Qt.QSize(40, 40))
        create_button.setMenu(create_menu)

        self.widget = Qt.QWidget()

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
        layout.addWidget(self.widget)
        self.setLayout(layout)

    def display_question(self, question_data):
        """
        Displays current question.
        """
        self.question_id = question_data['rowid'] if question_data else -1
        self.refresh()
        old_widget = self.layout().itemAt(2).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        self.widget = self.app.get_question_widget(question_data)
        self.layout().addWidget(self.widget)

    def display_settings(self, exam_data):
        """
        Displays exam settings.
        """
        self.question_id = None
        self.refresh()
        old_widget = self.layout().itemAt(2).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        self.widget = self.app.get_settings_widget(exam_data)
        self.layout().addWidget(self.widget)

    def refresh(self):
        """
        Updates exam information and refreshes upper panel.
        """
        self.settings_button.setStyleSheet(common.upper_question_style(None, self.question_id))
        while self.questions_layout.count() > 0:
            old_widget = self.questions_layout.itemAt(0).widget()
            old_widget.deleteLater()
            self.questions_layout.removeWidget(old_widget)
        for question in range(len(self.questions_ids)):
            question_id = self.questions_ids[question]
            question_button = Qt.QPushButton(str(question + 1))
            question_button.setCursor(Qt.Qt.PointingHandCursor)
            question_button.setFixedSize(Qt.QSize(50, 50))
            question_button.clicked.connect(
                common.return_lambda(self.app.view_exam_question, question_id))
            question_button.setStyleSheet(
                common.upper_question_style(question_id, self.question_id))
            self.questions_layout.addWidget(question_button)
