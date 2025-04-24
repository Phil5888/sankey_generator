"""Store the configuration data for the Sankey Generator."""

import json


class IncomeFilter:
    """Model for a transaction source."""

    def __init__(self, sankey_label: str, csv_column_name: str):
        """Initialize the transaction source."""
        self.sankey_label: str = sankey_label
        self.csv_column_name: str = csv_column_name
        self.csv_value_filters: list[str] = []


class AccountSource:
    """Model for an income source."""

    def __init__(self, account_name: str, iban: str):
        """Initialize the income source."""
        self.account_name: str = account_name
        self.iban: str = iban
        # Income filters are required to ignore transactions from one account to the other
        self.income_filters: list[IncomeFilter] = []
        # TODO: Do issue filters make sense?

    def add_income_filter(self, income_source: IncomeFilter):
        """Add an income source to the list of income sources."""
        self.income_filters.append(income_source)


class DataFrameFilter:
    """Model for a DataFrame filter."""

    def __init__(self, csv_column_name: str, csv_value_filters: list[str]):
        """Initialize the DataFrame filter."""
        self.csv_column_name: str = csv_column_name
        self.csv_value_filters: str = csv_value_filters


class IssueCategory:
    """Model for an issue category."""

    def __init__(self, csv_column_name: str):
        """Initialize the issue category."""
        self.csv_column_name: str = csv_column_name
        self.sub_category: IssueCategory = None

    def add_sub_category(self, sub_category: 'IssueCategory'):
        """Add a sub issue to the issue category."""
        self.sub_category = sub_category

    def get_depth(self) -> int:
        """Get the depth of the issue category."""
        if not self.sub_category:
            return 1
        return 1 + self.sub_category.get_depth()


class Config:
    """Store the configuration data for the Sankey Generator."""

    def __init__(self, config_file):
        """Initialize the configuration data."""
        with open(config_file, 'r') as file:
            config_data = json.load(file)

        self.input_file = config_data['input_file']
        self.output_file = config_data['output_file']
        # self.income_reference_accounts = config_data['income_reference_accounts']
        # self.income_sources = config_data['income_sources']
        self.income_reference_accounts: list[AccountSource] = []
        for account in config_data['income_reference_accounts']:
            account_source = AccountSource(account['account_name'], account['iban'])
            for income_filter in account['income_filters']:
                transaction_source = IncomeFilter(income_filter['sankey_label'], income_filter['csv_column_name'])
                transaction_source.csv_value_filters = income_filter.get('csv_value_filters', [])
                account_source.add_income_filter(transaction_source)
            self.income_reference_accounts.append(account_source)

        # self.income_data_frame_filters = config_data['income_data_frame_filters']
        # self.issues_data_frame_filters = config_data['issues_data_frame_filters']

        self.income_data_frame_filters: list[DataFrameFilter] = []
        for filter in config_data['income_data_frame_filters']:
            self.income_data_frame_filters.append(
                DataFrameFilter(filter['csv_column_name'], filter['csv_value_filters'])
            )
        self.issues_data_frame_filters: list[DataFrameFilter] = []
        for filter in config_data['issues_data_frame_filters']:
            self.issues_data_frame_filters.append(
                DataFrameFilter(filter['csv_column_name'], filter['csv_value_filters'])
            )
        # self.column_analysis_main_category = config_data['column_analysis_main_category']
        # self.column_analysis_sub_category = config_data['column_analysis_sub_category']
        self.issues_hierarchy: IssueCategory = self._getIssuesHierarchy(config_data['issues_hierarchy'])

        self.income_node_name = config_data['income_node_name']
        self.not_used_income_names = config_data['not_used_income_names']
        self.analysis_year_column_name = config_data['analysis_year_column_name']
        self.analysis_month_column_name = config_data['analysis_month_column_name']
        self.amount_out_name = config_data['amount_out_name']
        self.other_income_name = config_data['other_income_name']
        self.last_used_month = config_data['last_used_month']
        self.last_used_year = config_data['last_used_year']
        self.last_used_issue_level = config_data['last_used_issue_level']
        self.dark_mode = config_data['dark_mode']

    def _getIssuesHierarchy(self, issues_hierarchy: list[dict]) -> IssueCategory:
        """Create the issues hierarchy from the config file."""
        if issues_hierarchy is None:
            return None
        issue_category = IssueCategory(issues_hierarchy['csv_column_name'])
        sub_category = issues_hierarchy.get('sub_category')
        if sub_category is not None:
            issue_category.add_sub_category(self._getIssuesHierarchy(sub_category))

        return issue_category
