from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)
import sys
from sankey_generator.models.csv_filter import CsvFilter
from sankey_generator.models.data_frame_filter import DataFrameFilter
from sankey_generator.finanzguru_csv_parser import FinanzguruCsvParser
from sankey_generator.sankey_plotter import SankeyPlotter
from sankey_generator.models.theme import Theme
from sankey_generator.models.config import Config
import os.path
import platform
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QTimer
import plotly.io as pio

from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineCore import QWebEngineSettings


class MainWindow(QMainWindow):
    # TODO List:
    # - Add a way to select the input file
    # - Add a way to select the output file
    # - Add a way to select the reference accounts
    # - Add a way to select the income sources
    # - Add a way to select the income node name
    # - Add a way to select the not used income names
    # - Add a way to select the analysis year column name
    # - Add a way to select the analysis month column name
    # - Add a way to select the amount out name
    # - Add a way to select the other income name
    # - Add a way to select the issue level
    # - Add a way to select the income data frame filters
    # - Add a way to select the issues data frame filters
    # - Add a way to select the income reference accounts
    # - Add a way to select the issues reference accounts
    # - Add a config file to save the settings
    # - Add budget indecator to sankey diagram
    # - Split income to reference accounts (Requires ignoring "Umbuchung" in the CSV)
    # - Add subcategories for fix costs and variable costs
    # - Create a diagramm only for fix costs and variable costs

    # Load configuration
    config = Config('config.json')

    # Create required folders
    os.makedirs('input_files', exist_ok=True)
    os.makedirs('output_files', exist_ok=True)

    # Configure parser and plotter
    fcp = FinanzguruCsvParser(
        config.column_analysis_main_category,
        config.column_analysis_sub_category,
        config.analysis_year_column_name,
        config.analysis_month_column_name,
        config.income_node_name,
        config.amount_out_name,
        config.other_income_name,
        config.not_used_income_names,
    )
    sp = SankeyPlotter(config.amount_out_name)

    income_sources = [CsvFilter(src['label'], src['column'], src['values']) for src in config.income_sources]

    income_data_frame_filters = [
        DataFrameFilter(flt['column'], flt['values']) for flt in config.income_data_frame_filters
    ]

    issues_data_frame_filters = [
        DataFrameFilter(flt['column'], flt['values']) for flt in config.issues_data_frame_filters
    ]

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sankey Diagram Generator')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText('2025')
        self.year_input.text = '2025'

        self.layout.addWidget(self.year_input)

        self.month_input = QLineEdit(self)
        self.month_input.setPlaceholderText('1')
        self.month_input.text = '1'
        self.layout.addWidget(self.month_input)

        self.issue_level_input = QLineEdit(self)
        self.issue_level_input.setPlaceholderText('1')
        self.issue_level_input.text = '1'
        self.layout.addWidget(
            self.issue_level_input,
        )

        self.generate_button = QPushButton('Start Sankey generation', self)
        self.generate_button.clicked.connect(self.on_submit)
        self.layout.addWidget(self.generate_button)

        self.diagram_browser = QWebEngineView()  # = QLabel('Sankey diagram will be displayed here.', self)
        # Enable JavaScript in WebView
        self.diagram_browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        self.diagram_browser.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
        )
        self.layout.addWidget(self.diagram_browser)

        self.central_widget.setLayout(self.layout)

    def generate_sankey(self, year, month, issue_level):
        """Generate the Sankey diagram for the given year, month and issue level."""
        # Parse CSV and plot Sankey diagram
        income_node = self.fcp.parse_csv(
            self.config.input_file,
            self.income_sources,
            year,
            month,
            issue_level,
            self.income_data_frame_filters,
            self.issues_data_frame_filters,
        )

        # Generate the interactive Sankey diagram as an HTML div
        fig = self.sp.get_sankey_fig(income_node, year, month)

        print('Sankey generated')

        return fig

    def on_submit(self):
        year = self.year_input.text
        month = self.month_input.text
        issue_level = self.issue_level_input.text

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
