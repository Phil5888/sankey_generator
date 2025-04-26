"""Main window of the Sankey Diagram Generator."""

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from sankey_generator.ui.animated_toggle import AnimatedToggle
from sankey_generator.controllers.main_controller import MainController
from PyQt6.QtWebEngineCore import QWebEngineProfile
from sankey_generator.utils.observer import Observer, ObserverKeys
from PyQt6.QtCore import QUrl


class MainWindow(QMainWindow, Observer):
    """Main window of the Sankey Diagram Generator."""

    def __init__(self, controller: MainController):
        """Initialize the main window."""
        super().__init__()
        self.controller: MainController = controller
        self.config = controller.config_service.config
        self._init_ui()

    def update(self, observable, *args, **kwargs):
        """Update method for the observer pattern."""
        if observable == self.controller:
            if args[0] == ObserverKeys.SANKEY_GENERATED and isinstance(args[1], QUrl):
                # Update the browser with the new HTML content
                self.diagram_browser.setUrl(args[1])
            if args[0] == ObserverKeys.THEME_CHANGED and isinstance(args[1], str):
                # Update the theme
                self.setStyleSheet(args[1])
                self.controller.create_and_add_sankey()
        else:
            raise ValueError(f'Unknown observable: {observable}')

    def _init_ui(self):
        """Create the user interface."""
        self.setWindowTitle('Sankey Generator')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(self.controller.theme_manager.get_stylesheet())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout (Vertical)
        self.layout: QVBoxLayout = QVBoxLayout()

        # Section: Title
        self.layout.addWidget(QLabel('Sankey Diagram Generator', self))
        self.layout.addWidget(QLabel('Please enter the following information:', self))

        # Input Layout
        input_layout: QVBoxLayout = QVBoxLayout()

        # Year Input
        input_layout.addWidget(QLabel('Year'))
        self.year_input = self._create_input_field('Year', self.config.last_used_year, self.controller.set_year)
        input_layout.addWidget(self.year_input)

        # Month Input
        input_layout.addWidget(QLabel('Month'))
        self.month_input = self._create_input_field('Month', self.config.last_used_month, self.controller.set_month)
        input_layout.addWidget(self.month_input)

        # Issue Level Input
        input_layout.addWidget(QLabel('Issue Level'))
        self.issue_level_input = self._create_input_field(
            'Issue Level', self.config.last_used_issue_level, self.controller.set_issue_level
        )
        input_layout.addWidget(self.issue_level_input)

        # Generate Button
        self.generate_button = self._create_button('Start Sankey generation', self.controller.on_generate_sankey)
        input_layout.addWidget(self.generate_button)

        # Dark Mode Switch
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setSpacing(10)
        horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        horizontal_layout.addWidget(QLabel('Dark Mode'))
        self.toggle_switch: AnimatedToggle = self._create_dark_mode_switch()
        horizontal_layout.addWidget(self.toggle_switch)
        input_layout.addLayout(horizontal_layout)

        # Add input layout to the main layout
        self.layout.addLayout(input_layout, stretch=1)

        # Browser Section
        self.diagram_browser = self._create_browser()
        self.layout.addWidget(self.diagram_browser, stretch=5)

        self.central_widget.setLayout(self.layout)

    def _create_dark_mode_switch(self) -> AnimatedToggle:
        """Create a dark mode switch."""
        toggle_switch = AnimatedToggle()
        toggle_switch.setFixedSize(toggle_switch.sizeHint())
        toggle_switch.setChecked(self.config.dark_mode)
        toggle_switch.stateChanged.connect(self.controller.on_toggle_theme)
        return toggle_switch

    def _create_input_field(self, placeholder_text: str, default_value: str, save_func) -> QLineEdit:
        """Create an input field with the given placeholder text and default value."""
        input_field = QLineEdit(self)
        input_field.setPlaceholderText(placeholder_text)
        input_field.setText(str(default_value))
        input_field.textChanged.connect(lambda text: save_func(text))
        return input_field

    def _create_button(self, text, on_click) -> QPushButton:
        """Create a button with the given text and on_click function."""
        button = QPushButton(text, self)
        button.clicked.connect(on_click)

        return button

    def _create_browser(self) -> QWebEngineView:
        """Create a browser to display the Sankey diagram."""
        browser = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        # Handle download requests
        profile.downloadRequested.connect(self.controller.on_download_requested)
        browser.setHtml(self.controller.get_html())

        return browser
