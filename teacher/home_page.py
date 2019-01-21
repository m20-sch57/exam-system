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
    def __init__(self, widget_map):
        super().__init__()
        self.widget_map = widget_map

        self.upper_layout = Qt.QHBoxLayout()

        layout = Qt.QVBoxLayout()
        layout.addLayout(self.upper_layout)
        layout.addSpacerItem(Qt.QSpacerItem(0, 20))
        layout.addWidget(Qt.QWidget())
        self.setLayout(layout)

    def display(self, current_widget_name):
        """
        Displays the widget.
        """
        while self.upper_layout.count() > 0:
            old_widget = self.upper_layout.itemAt(0).widget()
            old_widget.deleteLater()
            self.upper_layout.removeWidget(old_widget)

        for widget_name in self.widget_map.keys():
            widget_button = FlatButton(widget_name)
            widget_button.setFont(Qt.QFont('Arial', 20))
            widget_button.clicked.connect(
                common.return_lambda(self.display, widget_name))
            if widget_name == current_widget_name:
                widget_button.setStyleSheet(
                    'color: blue;'
                    'border-bottom: 2px solid blue;'
                )
            self.upper_layout.addWidget(widget_button)

        main_widget = self.widget_map[current_widget_name]()
        old_widget = self.layout().itemAt(2).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        self.layout().addWidget(main_widget)
