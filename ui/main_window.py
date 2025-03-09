"""Main window of the Sankey Diagram Generator."""

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

from sankey_generator.models.csv_filter import CsvFilter
from sankey_generator.models.data_frame_filter import DataFrameFilter
from sankey_generator.finanzguru_csv_parser import FinanzguruCsvParser
from sankey_generator.sankey_plotter import SankeyPlotter
from sankey_generator.models.config import Config
import os.path
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.io as pio

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

        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText('Year')
        self.year_input.setText(str(config.last_used_year))

        self.layout.addWidget(self.year_input)

        self.month_input = QLineEdit(self)
        self.month_input.setPlaceholderText('Month')
        self.month_input.setText(str(config.last_used_month))
        self.layout.addWidget(self.month_input)

        self.issue_level_input = QLineEdit(self)
        self.issue_level_input.setPlaceholderText('Issue Level')
        self.issue_level_input.setText(str(config.last_used_issue_level))
        self.layout.addWidget(
            self.issue_level_input,
        )

        self.generate_button = QPushButton('Start Sankey generation', self)
        self.generate_button.clicked.connect(self.on_submit)
        self.layout.addWidget(self.generate_button)

        self.diagram_browser = QWebEngineView()

        profile = QWebEngineProfile.defaultProfile()

        # Handle download requests
        profile.downloadRequested.connect(self.on_download_requested)
        self.layout.addWidget(self.diagram_browser)

        self.central_widget.setLayout(self.layout)

    def on_download_requested(self, download_item: QWebEngineDownloadRequest):
        """Handle download requests."""
        download_path = QDir.currentPath() + '/output_files'
        QDir().mkpath(download_path)
        download_item.setDownloadDirectory(download_path)
        download_item.setDownloadFileName('sankey.png')
        download_item.accept()  # Accept the download request, otherwise the download will not start

    def generate_sankey(self, year, month, issue_level):
        """Generate the Sankey diagram for the given year, month and issue level."""
        # Parse CSV and plot Sankey diagram
        income_node = self.fcp.parse_csv(
            year,
            month,
            issue_level,
        )

        # Generate the interactive Sankey diagram as an HTML div
        fig = self.sp.get_sankey_fig(income_node, year, month)

        print('Sankey generated')

        return fig

    def on_submit(self):
        """Handle the submit button click."""
        year = self.year_input.text()
        month = self.month_input.text()
        issue_level = self.issue_level_input.text()

        if not year or not month or not issue_level:
            QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
            return

        fig = self.generate_sankey(int(year), int(month), int(issue_level))
        # html = fig.to_html(full_html=True)
        html = pio.to_html(fig, full_html=True)

        # Save the HTML to a temporary file
        temp_file = 'temp_plot.html'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(html)

        # Load the file in WebView
        self.diagram_browser.setUrl(QUrl.fromLocalFile(os.path.abspath(temp_file)))

        print(f'Generating Sankey diagram for {year}-{month} with issue level {issue_level}')
