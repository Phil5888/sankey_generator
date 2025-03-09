"""Main window of the Sankey Diagram Generator."""

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QCheckBox,
    QMessageBox,
    QPushButton,
    QLabel,
)

from sankey_generator.finanzguru_csv_parser import FinanzguruCsvParser
from sankey_generator.sankey_plotter import SankeyPlotter
from sankey_generator.models.config import Config
from sankey_generator.models.theme import Theme
import os.path
from PyQt6.QtWebEngineWidgets import QWebEngineView

from PyQt6.QtCore import QUrl, QDir
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineDownloadRequest


class MainWindow(QMainWindow):
    """Main window of the Sankey Diagram Generator."""

    def __init__(self, fcp: FinanzguruCsvParser, sp: SankeyPlotter, config: Config):
        """Initialize the main window."""
        super().__init__()
        self.fcp = fcp
        self.sp = sp
        self.config = config
        self.current_year = None
        self.current_month = None
        self.current_issue_level = None
        self._init_ui()

    def _init_ui(self):
        """Create the user interface."""
        self.setWindowTitle('Sankey Generator')
        self.setGeometry(100, 100, 800, 600)
        self._apply_theme()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout (Vertical)
        self.layout: QVBoxLayout = QVBoxLayout()

        # Section: Title
        self.layout.addWidget(QLabel('Sankey Diagram Generator', self))
        self.layout.addWidget(QLabel('Please enter the following information:', self))

        # Input Layout (Smaller section)
        input_layout: QVBoxLayout = QVBoxLayout()

        # Year
        input_layout.addWidget(QLabel('Year'))
        self.year_input = self._create_input_field('Year', self.config.last_used_year)
        input_layout.addWidget(self.year_input)

        # Month
        input_layout.addWidget(QLabel('Month'))
        self.month_input = self._create_input_field('Month', self.config.last_used_month)
        input_layout.addWidget(self.month_input)

        # Issue Level
        input_layout.addWidget(QLabel('Issue Level'))
        self.issue_level_input = self._create_input_field('Issue Level', self.config.last_used_issue_level)
        input_layout.addWidget(self.issue_level_input)

        # Generate Button
        self.generate_button = self._create_button('Start Sankey generation', self._on_submit)
        input_layout.addWidget(self.generate_button)

        # Toggle Switch
        input_layout.addWidget(self._create_dark_mode_switch())

        # Add input layout to the main layout with a small stretch
        self.layout.addLayout(input_layout, stretch=1)

        # Section: Browser (Should take most of the space)
        self.diagram_browser = self._create_browser()
        self.layout.addWidget(self.diagram_browser, stretch=5)  # This will expand more than inputs

        self.central_widget.setLayout(self.layout)

    def _apply_theme(self):
        """Apply the current theme to the main window."""
        colors = Theme.get_colors()

        with open('theme.qss', 'r') as file:
            stylesheet = file.read().format(**colors)

        self.setStyleSheet(stylesheet)
        self._create_and_add_sankey()

    def _toggle_theme(self):
        """Toggle the theme between dark and light mode."""
        Theme.toggle_mode()
        if self.diagram_browser:
            self.diagram_browser.setHtml(self._get_html())
        self._apply_theme()

    def _on_download_requested(self, download_item: QWebEngineDownloadRequest) -> None:
        """Handle download requests."""
        download_path = QDir.currentPath() + '/output_files'
        QDir().mkpath(download_path)
        download_item.setDownloadDirectory(download_path)
        download_item.setDownloadFileName('sankey.png')
        download_item.accept()  # Accept the download request, otherwise the download will not start

    def _create_dark_mode_switch(self) -> QCheckBox:
        """Create a dark mode switch."""
        toggle_switch = QCheckBox('Dark Mode', self)
        toggle_switch.setChecked(Theme.dark_mode)
        toggle_switch.stateChanged.connect(self._toggle_theme)

        return toggle_switch

    def _create_input_field(self, placeholder_text, default_value) -> QLineEdit:
        """Create an input field with the given placeholder text and default value."""
        input_field = QLineEdit(self)
        input_field.setPlaceholderText(placeholder_text)
        input_field.setText(str(default_value))

        return input_field

    def _create_browser(self) -> QWebEngineView:
        """Create a browser to display the Sankey diagram."""
        browser = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        # Handle download requests
        profile.downloadRequested.connect(self._on_download_requested)
        browser.setHtml(self._get_html())

        return browser

    def _create_button(self, text, on_click) -> QPushButton:
        """Create a button with the given text and on_click function."""
        button = QPushButton(text, self)
        button.clicked.connect(on_click)

        return button

    def _on_submit(self) -> None:
        """Handle the submit button click."""
        self.current_year = self.year_input.text()
        self.current_month = self.month_input.text()
        self.current_issue_level = self.issue_level_input.text()

        if not self.current_year or not self.current_month or not self.current_issue_level:
            QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
            return
        self._create_and_add_sankey()

    def _get_html(self, content: str = '') -> str:
        """Get the HTML content with the given content."""
        return f'<html><body style="background-color: {Theme.get_colors()["background"]};">{content}</body></html>'

    def _create_and_add_sankey(self):
        if not self.current_year or not self.current_month or not self.current_issue_level:
            return

        fig_html = self.generate_sankey_html(
            int(self.current_year), int(self.current_month), int(self.current_issue_level)
        )

        # Save the HTML to a temporary file
        temp_file = 'temp_plot.html'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(self._get_html(fig_html))

        # Load the file in WebView
        self.diagram_browser.setUrl(QUrl.fromLocalFile(os.path.abspath(temp_file)))

        print(
            f'Generating Sankey diagram for {self.current_year}-{self.current_month} with issue level {self.current_issue_level}'
        )

    def generate_sankey_html(self, year, month, issue_level) -> str:
        """Generate the Sankey diagram for the given year, month and issue level."""
        # Parse CSV and plot Sankey diagram
        income_node = self.fcp.parse_csv(
            year,
            month,
            issue_level,
        )

        # Generate the interactive Sankey diagram as an HTML div
        fig_html = self.sp.get_sankey_html(income_node, year, month)

        print('Sankey generated')

        return fig_html
