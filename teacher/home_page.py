"""
Teacher's home page.
"""


from PyQt5 import Qt
import common


class HomePage(Qt.QWidget):
    """
    Teacher's home page.
    """
    def __init__(self, app, widget_map):
        super().__init__()
        self.widget_map = widget_map

        view_profile_action = Qt.QWidgetAction(self)
        view_profile_action.setFont(Qt.QFont('Arial', 15))
        view_profile_action.setText('Профиль')
        view_profile_action.triggered.connect(lambda _: app.logout())

        exit_action = Qt.QWidgetAction(self)
        exit_action.setFont(Qt.QFont('Arial', 15))
        exit_action.setText('Выйти')
        exit_action.triggered.connect(lambda _: app.logout())

        user_menu = Qt.QMenu(self)
        user_menu.addAction(view_profile_action)
        user_menu.addAction(exit_action)

        user_button = Qt.QPushButton(Qt.QIcon(common.USER), '', self)
        user_button.setObjectName('Flat')
        user_button.setCursor(Qt.Qt.PointingHandCursor)
        user_button.setIconSize(Qt.QSize(35, 35))
        user_button.setFixedSize(Qt.QSize(55, 55))
        user_button.setMenu(user_menu)

        self.widget_layout = Qt.QHBoxLayout()
        self.widget_layout.setSpacing(0)

        upper_layout = Qt.QHBoxLayout()
        upper_layout.addLayout(self.widget_layout)
        upper_layout.addWidget(user_button)

        upper_panel = Qt.QFrame(self)
        upper_panel.setLayout(upper_layout)

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
            widget_button = Qt.QPushButton(widget_name, self)
            widget_button.setObjectName('Link')
            widget_button.setCursor(Qt.Qt.PointingHandCursor)
            widget_button.setFont(Qt.QFont('Arial', 20))
            widget_button.clicked.connect(
                common.return_lambda(self.display, widget_name))
            if widget_name == current_widget_name:
                widget_button.setStyleSheet(
                    'color: #2CA9FD;'
                    'border-bottom: 3px solid #2CA9FD;'
                )
            self.widget_layout.addWidget(widget_button)

        main_widget = self.widget_map[current_widget_name]()
        old_widget = self.layout().itemAt(2).widget()
        old_widget.deleteLater()
        self.layout().removeWidget(old_widget)
        self.layout().addWidget(main_widget)
