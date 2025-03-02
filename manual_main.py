"""Main module for the sankey_generator package."""

from sankey_generator.models.csv_filter import CsvFilter
from sankey_generator.models.data_frame_filter import DataFrameFilter
from sankey_generator.finanzguru_csv_parser import FinanzguruCsvParser
from sankey_generator.models.sankey_income_node import SankeyIncomeNode
from sankey_generator.sankey_plotter import SankeyPlotter
from sankey_generator.models.config import Config
import os


def main():
    """Run the main module."""
    # Load configuration
    config = Config('config.json')

    # create required folders
    os.makedirs('input_files', exist_ok=True)
    os.makedirs('output_files', exist_ok=True)

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

    year = 2024
    month = 3
    issue_level = 2

    income_node: SankeyIncomeNode = fcp.parse_csv(
        config.input_file,
        income_sources,
        year,
        month,
        issue_level,
        income_data_frame_filters,
        issues_data_frame_filters,
    )

    sankey_html = sp.get_sankey_html(income_node, year, month)

    with open('output_files/sankey.html', 'w') as file:
        file.write(sankey_html)


if __name__ == '__main__':
    main()
