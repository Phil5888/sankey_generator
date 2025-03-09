"""App startup."""

import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from sankey_generator.models.csv_filter import CsvFilter
from sankey_generator.models.data_frame_filter import DataFrameFilter
from sankey_generator.finanzguru_csv_parser import FinanzguruCsvParser
from sankey_generator.sankey_plotter import SankeyPlotter
from sankey_generator.models.config import Config


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
# - use colors from Theme
# - Add dark / light mode switch
# - Fix white boarder around sankey diagram


if __name__ == '__main__':
    # Load configuration
    config = Config('config.json')

    # Create required folders
    os.makedirs('input_files', exist_ok=True)
    os.makedirs('output_files', exist_ok=True)

    # Configure parser and plotter
    sp = SankeyPlotter(config.amount_out_name)

    income_sources = [CsvFilter(src['label'], src['column'], src['values']) for src in config.income_sources]
    income_data_frame_filters = [
        DataFrameFilter(flt['column'], flt['values']) for flt in config.income_data_frame_filters
    ]
    issues_data_frame_filters = [
        DataFrameFilter(flt['column'], flt['values']) for flt in config.issues_data_frame_filters
    ]
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
    fcp.configure_parser(config.input_file, income_sources, income_data_frame_filters, issues_data_frame_filters)

    app = QApplication(sys.argv)
    window = MainWindow(fcp, sp)
    window.show()
    sys.exit(app.exec())
