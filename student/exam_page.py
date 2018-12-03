"""
Page that is displayed when student is passing the exam.
"""


import os
from PyQt5.Qt import Qt, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.Qt import QLabel, QScrollArea
from PyQt5.Qt import QFont, QPixmap, QSize, QSizePolicy, QSpacerItem, QFrame
from mywidgets import Label, Pixmap


class ExamPage(QWidget):
    """
    Page that is displayed when student is passing the exam.
    """
    def __init__(self, exam, back_function):
        super().__init__()
        self.exam = exam
        self.question = None
        self.exam_data = None
        self.exam_info = None

        back_img = Pixmap(normal_pic=QPixmap(os.path.join('images', 'left-50x50.png')),
                          hover_pic=QPixmap(os.path.join('images', 'left-50x50.png')))
        back_img.setFixedSize(QSize(50, 50))
        back_img.clicked.connect(back_function)

        exam_title = QLabel(exam)
        exam_title.setFont(QFont('Arial', 30))
        exam_title.setAlignment(Qt.AlignCenter)
        exam_title.setWordWrap(True)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setMinimumHeight(85)
        scroll_area.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        status_widget = QWidget()
        question_widget = QWidget()

        self.questions_layout = QHBoxLayout()
        self.questions_layout.setSpacing(0)

        scroll_layout = QHBoxLayout()
        scroll_layout.addLayout(self.questions_layout)
        scroll_layout.addStretch(1)

        scroll_widget = QWidget()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)

        upper_layout = QHBoxLayout()
        upper_layout.addWidget(back_img)
        upper_layout.addWidget(exam_title)

        layout = QVBoxLayout()
        layout.addLayout(upper_layout)
        layout.addSpacerItem(QSpacerItem(0, 10))
        layout.addWidget(scroll_area)
        layout.addWidget(status_widget)
        layout.addWidget(question_widget)
        self.setLayout(layout)

    def display(self, current_question, exam_data, exam_info, view_question_function,
                get_exam_status_function, get_question_function):
        """
        Displays current question.
        """
        self.question = current_question
        self.exam_data = exam_data
        self.exam_info = exam_info

        while self.questions_layout.count() > 0:
            old_widget = self.questions_layout.itemAt(0).widget()
            old_widget.deleteLater()
            self.questions_layout.removeWidget(old_widget)

        for question in range(1, len(exam_data) + 1):
            question_data = exam_data[question - 1]
            question_label = Label(str(question))
            question_label.setFont(QFont('Arial', 20))
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setFixedSize(QSize(50, 50))
            question_label.connect(view_question_function, self.exam, question)

            self.questions_layout.addWidget(question_label)

            if question == current_question:
                question_label.setStyleSheet(
                    'color: blue;'
                    'background: #CCE8FF;'
                    'border-style: solid;'
                    'border-width: 1px;'
                    'border-color: #99D1FF')
            else:
                if question_data['score'] is False:
                    background = 'white'
                elif int(question_data['score']) == int(question_data['maxscore']):
                    background = '#9CFB8E' # correct
                else:
                    background = '#F94D51' # incorrect
                question_label.setStyleSheet(
                    'background: ' + background + ';'
                    'border-style: solid;'
                    'border-width: 1px')

        status_widget = get_exam_status_function(self)
        question_widget = get_question_function(self)
        old_widget = self.layout().itemAt(4).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        old_widget = self.layout().itemAt(3).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        self.layout().addWidget(status_widget)
        self.layout().addWidget(question_widget)