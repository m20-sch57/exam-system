"""
Widget for home page with list of messages.
"""


from PyQt5 import Qt


class MessagesWidget(Qt.QWidget):
    """
    Widget for home page with list of messages.
    """
    def __init__(self):
        super().__init__()

        layout = Qt.QVBoxLayout()
        layout.addStretch(1)
        self.setLayout(layout)
