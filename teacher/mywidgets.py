"""
Contains my widgets.
"""


from PyQt5 import Qt


class FlatButton(Qt.QPushButton):
    """
    Link with text and picture.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(Qt.Qt.PointingHandCursor)
