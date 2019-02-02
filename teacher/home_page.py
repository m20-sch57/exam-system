"""
Teacher's home page.
"""


from PyQt5 import Qt
from mywidgets import FlatButton
import common


class HomePage(Qt.QWidget):
    """
    Teacher's home page.
    """
    def __init__(self, widget_map, exit_function):
        super().__init__()
        self.widget_map = widget_map

        exit_button = FlatButton(Qt.QIcon(common.USER), '')
        exit_button.setIconSize(Qt.QSize(40, 40))
        exit_button.setFixedSize(exit_button.sizeHint())
        exit_button.clicked.connect(lambda _: exit_function())

        self.widget_layout = Qt.QHBoxLayout()
        self.widget_layout.setSpacing(0)

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addLayout(self.widget_layout)
        upper_layout.addWidget(exit_button)

        upper_panel = Qt.QFrame()
        upper_panel.setLayout(upper_layout)
        upper_panel.setStyleSheet('background: #f5f5f5')

        layout = Qt.QVBoxLayout()
        layout.addWidget(upper_panel)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(Qt.QWidget())
        self.setLayout(layout)

    def display(self, current_widget_name):
        """
        Displays the widget.
        """
        while self.widget_layout.count() > 0:
            old_widget = self.widget_layout.itemAt(0).widget()
            old_widget.deleteLater()
            self.widget_layout.removeWidget(old_widget)

        for widget_name in self.widget_map.keys():
            widget_button = FlatButton(widget_name)
            widget_button.setFont(Qt.QFont('Arial', 20))
            widget_button.clicked.connect(
                common.return_lambda(self.display, widget_name))
            if widget_name == current_widget_name:
                widget_button.setStyleSheet(
                    'color: blue;'
                    'border-bottom: 3px solid blue;'
                )
            self.widget_layout.addWidget(widget_button)

        main_widget = self.widget_map[current_widget_name]()
        old_widget = self.layout().itemAt(2).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        self.layout().addWidget(main_widget)
