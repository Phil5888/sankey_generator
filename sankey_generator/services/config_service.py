"""Service to handle the configuration data for the Sankey Generator."""

import json
from sankey_generator.models.config import Config, DataFrameFilter, AccountSource, IssueCategory, IncomeFilter
import os


class ConfigService:
    """Store the configuration data for the Sankey Generator."""

    def __init__(self, config_file):
        """Initialize the configuration data."""
        # chek if the config file exists
        if not os.path.exists(config_file):
            # create a default config file
            default_config = {
                'input_file': '',
                'output_file': '',
                'income_reference_accounts': [],
                'income_data_frame_filters': [],
                'issues_data_frame_filters': [],
                'issues_hierarchy': [],
                'income_node_name': '',
                'not_used_income_name': '',
                'analysis_year_column_name': '',
                'analysis_month_column_name': '',
                'amount_out_name': '',
                'other_income_name': '',
                'last_used_month': 0,
                'last_used_year': 0,
                'last_used_issue_level': 0,
                'dark_mode': False,
            }
            with open(config_file, 'w') as file:
                json.dump(default_config, file, indent=4)

        with open(config_file, 'r') as file:
            config_data = json.load(file)

        self.config: Config = Config(
            input_file=config_data['input_file'],
            output_file=config_data['output_file'],
            income_reference_accounts=self._parseIncomeReferenceAccounts(config_data['income_reference_accounts']),
            income_data_frame_filters=self._parseDataFrameFilter(config_data['income_data_frame_filters']),
            issues_data_frame_filters=self._parseDataFrameFilter(config_data['issues_data_frame_filters']),
            issues_hierarchy=self._parseIssuesHierarchy(config_data['issues_hierarchy']),
            income_node_name=config_data['income_node_name'],
            not_used_income_name=config_data['not_used_income_name'],
            analysis_year_column_name=config_data['analysis_year_column_name'],
            analysis_month_column_name=config_data['analysis_month_column_name'],
            amount_out_name=config_data['amount_out_name'],
            other_income_name=config_data['other_income_name'],
            last_used_month=config_data['last_used_month'],
            last_used_year=config_data['last_used_year'],
            last_used_issue_level=config_data['last_used_issue_level'],
            dark_mode=config_data['dark_mode'],
        )

    def _parseDataFrameFilter(self, issues_data_frame_filter: dict) -> DataFrameFilter:
        """Create the data frame filters from the config file."""
        issues_data_frame_filters: list[DataFrameFilter] = []
        for filter in issues_data_frame_filter:
            issues_data_frame_filters.append(DataFrameFilter(filter['csv_column_name'], filter['csv_value_filters']))

        return issues_data_frame_filters

    def _parseIncomeReferenceAccounts(self, income_reference_accounts: dict) -> list[AccountSource]:
        """Create the income reference accounts from the config file."""
        income_reference_accounts: list[AccountSource] = []
        for account in income_reference_accounts:
            account_source = AccountSource(account['account_name'], account['iban'])
            for income_filter in account['income_filters']:
                transaction_source = IncomeFilter(income_filter['sankey_label'], income_filter['csv_column_name'])
                transaction_source.csv_value_filters = income_filter.get('csv_value_filters', [])
                account_source.income_filters.append(transaction_source)
            income_reference_accounts.append(account_source)

        return income_reference_accounts

    def _parseIssuesHierarchy(self, issues_hierarchy: list[dict]) -> IssueCategory:
        """Create the issues hierarchy from the config file."""
        if issues_hierarchy is None or len(issues_hierarchy) == 0:
            return None
        issue_category = IssueCategory(issues_hierarchy['csv_column_name'])
        sub_category = issues_hierarchy.get('sub_category')
        if sub_category is not None:
            issue_category.sub_category = self._parseIssuesHierarchy(sub_category)

        return issue_category

    def _save_config(self):
        """Save the configuration data to the config file."""
        with open('config.json', 'w') as file:
            json.dump(self.config.to_dict(), file, indent=4)

    def _save_string_value(self, key: str, new_value: str) -> None:
        """Save a string value to the config file."""
        setattr(self.config, key, new_value)
        self._save_config()

    def _save_int_value(self, key: str, new_value: int) -> None:
        """Save an integer value to the config file."""
        setattr(self.config, key, new_value)
        self._save_config()

    def save_dark_mode(self, dark_mode: bool) -> None:
        """Save the dark mode value to the config file."""
        self._save_string_value('dark_mode', dark_mode)

    def save_last_used_month(self, last_used_month: int) -> None:
        """Save the last used month value to the config file."""
        self._save_int_value('last_used_month', last_used_month)

    def save_last_used_year(self, last_used_year: int) -> None:
        """Save the last used year value to the config file."""
        self._save_int_value('last_used_year', last_used_year)

    def save_last_used_issue_level(self, last_used_issue_level: int) -> None:
        """Save the last used issue level value to the config file."""
        self._save_int_value('last_used_issue_level', last_used_issue_level)
