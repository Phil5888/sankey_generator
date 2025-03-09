"""Main window of the Sankey Diagram Generator."""

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

from sankey_generator.finanzguru_csv_parser import FinanzguruCsvParser
from sankey_generator.sankey_plotter import SankeyPlotter
from sankey_generator.models.config import Config
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

        self.setWindowTitle('Sankey Diagram Generator')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout: QVBoxLayout = QVBoxLayout()

        self.year_input = self.create_input_field('Year', config.last_used_year)
        self.layout.addWidget(self.year_input)

        self.month_input = self.create_input_field('Month', config.last_used_month)
        self.layout.addWidget(self.month_input)

        self.issue_level_input = self.create_input_field('Issue Level', config.last_used_issue_level)
        self.layout.addWidget(self.issue_level_input)

        self.generate_button = self.create_button('Start Sankey generation', self.on_submit)
        self.layout.addWidget(self.generate_button)

        self.diagram_browser = self.create_browser()
        self.layout.addWidget(self.diagram_browser)

        self.central_widget.setLayout(self.layout)

    def on_download_requested(self, download_item: QWebEngineDownloadRequest):
        """Handle download requests."""
        download_path = QDir.currentPath() + '/output_files'
        QDir().mkpath(download_path)
        download_item.setDownloadDirectory(download_path)
        download_item.setDownloadFileName('sankey.png')
        download_item.accept()  # Accept the download request, otherwise the download will not start

    def create_input_field(self, placeholder_text, default_value):
        """Create an input field with the given placeholder text and default value."""
        input_field = QLineEdit(self)
        input_field.setPlaceholderText(placeholder_text)
        input_field.setText(str(default_value))

        return input_field

    def create_browser(self):
        """Create a browser to display the Sankey diagram."""
        browser = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        # Handle download requests
        profile.downloadRequested.connect(self.on_download_requested)

        return browser

    def create_button(self, text, on_click):
        """Create a button with the given text and on_click function."""
        button = QPushButton(text, self)
        button.clicked.connect(on_click)

        return button

    def generate_sankey(self, year, month, issue_level):
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

    def on_submit(self):
        """Handle the submit button click."""
        year = self.year_input.text()
        month = self.month_input.text()
        issue_level = self.issue_level_input.text()

        if not year or not month or not issue_level:
            QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
            return

        fig_html = self.generate_sankey(int(year), int(month), int(issue_level))

        # Save the HTML to a temporary file
        temp_file = 'temp_plot.html'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(fig_html)

        # Load the file in WebView
        self.diagram_browser.setUrl(QUrl.fromLocalFile(os.path.abspath(temp_file)))

        print(f'Generating Sankey diagram for {year}-{month} with issue level {issue_level}')
