"""App startup."""

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from sankey_generator.controllers.main_controller import MainController
from sankey_generator.services.finanzguru_csv_parser_service import FinanzguruCsvParserService
from sankey_generator.services.sankey_plotter_service import SankeyPlotterService
from sankey_generator.services.config_service import ConfigService
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
# - Add proper validation


if __name__ == '__main__':
    app = QApplication(['Sankey Generator'])

    config_service: ConfigService = ConfigService('config.json')
    config: Config = config_service.config
    sankey_plotter_service: SankeyPlotterService = SankeyPlotterService(config.amount_out_name)

    finanzguru_parser_service: FinanzguruCsvParserService = FinanzguruCsvParserService(
        config.issues_hierarchy,
        config.analysis_year_column_name,
        config.analysis_month_column_name,
        config.income_node_name,
        config.amount_out_name,
        config.other_income_name,
        config.not_used_income_name,
    )
    finanzguru_parser_service.configure_parser(
        config.input_file,
        config.income_reference_accounts,
        config.income_data_frame_filters,
        config.issues_data_frame_filters,
    )

    # Initialize controller
    controller = MainController(config_service, finanzguru_parser_service, sankey_plotter_service)

    # Initialize and show main window
    window = MainWindow(controller)
    window.show()

    app.exec()
