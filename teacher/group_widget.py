"""
Widget for home page with group info.
"""


from PyQt5 import Qt


class GroupWidget(Qt.QWidget):
    """
    Widget for home page with group info.
    """
    def __init__(self):
        super().__init__()

        layout = Qt.QVBoxLayout()
        layout.addStretch(1)
        self.setLayout(layout)
