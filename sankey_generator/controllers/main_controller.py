"""MainController for the Sankey Generator application."""

from sankey_generator.services.theme_service import ThemeService
from sankey_generator.models.config import Config
from sankey_generator.services.config_service import ConfigService
from sankey_generator.services.finanzguru_csv_parser_service import FinanzguruCsvParserService
from sankey_generator.services.sankey_plotter_service import SankeyPlotterService
from PyQt6.QtWebEngineCore import QWebEngineDownloadRequest
from PyQt6.QtCore import QDir, QUrl
from sankey_generator.utils.observer import Observable
import os


class MainController(Observable):
    """Controller for the Sankey Generator application."""

    def __init__(
        self,
        config_service: ConfigService,
        parser_service: FinanzguruCsvParserService,
        plotter_service: SankeyPlotterService,
    ):
        """Initialize the main controller."""
        self.config_service: ConfigService = config_service
        self.finanzguru_parser_service: FinanzguruCsvParserService = parser_service
        self.sankey_plotter_service: SankeyPlotterService = plotter_service
        self.theme_manager: ThemeService = ThemeService(config_service)
        self.current_diagram_url: QUrl = None
        super().__init__()

    def save_year(self, year: str):
        """Save the last used year."""
        self.config_service.save_last_used_year(int(year))

    def save_month(self, month: str):
        """Save the last used month."""
        self.config_service.save_last_used_month(int(month))

    def save_issue_level(self, issue_level: str):
        """Save the last used issue level."""
        self.config_service.save_last_used_issue_level(int(issue_level))

    def toggle_theme(self):
        """Toggle the theme between dark and light mode."""
        self.theme_manager.toggle_theme()
        self.notify_observers('dark_mode', self.config_service.config.dark_mode)

    def get_initial_html(self) -> str:
        """Get the initial HTML content for the browser."""
        return '<html><body>Welcome to the Sankey Generator!</body></html>'

    def generate_sankey(self, year: int, month: int, issue_level: int) -> str:
        """Generate the Sankey diagram."""
        income_node = self.finanzguru_parser_service.parse_csv(year, month, issue_level)
        return self.sankey_plotter_service.get_sankey_html(income_node, year, month)

    def on_submit(self) -> None:
        """Handle the submit button click."""
        config: Config = self.config_service.config
        self.current_year = config.last_used_year
        self.current_month = config.last_used_month
        self.current_issue_level = config.last_used_issue_level

        # TODO: Replace with validation -> Disbale button on errors
        # if not self.current_year or not self.current_month or not self.current_issue_level:
        #     QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
        #     return
        self._create_and_add_sankey()

    def get_html(self, content: str = '') -> str:
        """Get the HTML content with the given content."""
        return f'<html><body style="background-color: {self.theme_manager.get_colors()["background"]};">{content}</body></html>'

    def _create_and_add_sankey(self):
        if not self.current_year or not self.current_month or not self.current_issue_level:
            return

        fig_html = self._generate_sankey_html(
            int(self.current_year), int(self.current_month), int(self.current_issue_level)
        )

        # Save the HTML to a temporary file
        temp_file = 'temp_plot.html'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(self.get_html(fig_html))

        # Load the file in WebView
        current_diagram_url: QUrl = QUrl.fromLocalFile(os.path.abspath(temp_file))
        # Notify observers about the new diagram URL
        self.notify_observers(current_diagram_url)

        print(
            f'Generating Sankey diagram for {self.current_year}-{self.current_month} with issue level {self.current_issue_level}'
        )

    def _generate_sankey_html(self, year, month, issue_level) -> str:
        """Generate the Sankey diagram for the given year, month and issue level."""
        # Parse CSV and plot Sankey diagram
        income_node = self.finanzguru_parser_service.parse_csv(
            year,
            month,
            issue_level,
        )

        # Generate the interactive Sankey diagram as an HTML div
        fig_html = self.sankey_plotter_service.get_sankey_html(income_node, year, month)

        print('Sankey generated')

        return fig_html

    def on_download_requested(self, download_item: QWebEngineDownloadRequest) -> None:
        """Handle download requests."""
        download_path = QDir.currentPath() + '/output_files'
        QDir().mkpath(download_path)
        download_item.setDownloadDirectory(download_path)
        download_item.setDownloadFileName('sankey.png')
        download_item.accept()  # Accept the download request, otherwise the download will not start
