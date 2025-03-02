"""Store the configuration data for the Sankey Generator."""

import json


class Config:
    """Store the configuration data for the Sankey Generator."""

    def __init__(self, config_file):
        """Initialize the configuration data."""
        with open(config_file, 'r') as file:
            config_data = json.load(file)

        self.input_file = config_data['input_file']
        self.output_file = config_data['output_file']
        self.income_reference_accounts = config_data['income_reference_accounts']
        self.income_sources = config_data['income_sources']
        self.income_data_frame_filters = config_data['income_data_frame_filters']
        self.issues_data_frame_filters = config_data['issues_data_frame_filters']
        self.column_analysis_main_category = config_data['column_analysis_main_category']
        self.column_analysis_sub_category = config_data['column_analysis_sub_category']
        self.income_node_name = config_data['income_node_name']
        self.not_used_income_names = config_data['not_used_income_names']
        self.analysis_year_column_name = config_data['analysis_year_column_name']
        self.analysis_month_column_name = config_data['analysis_month_column_name']
        self.amount_out_name = config_data['amount_out_name']
        self.other_income_name = config_data['other_income_name']
