"""Store the configuration data for the Sankey Generator."""


class IncomeFilter:
    """Model for a transaction source."""

    def __init__(self, sankey_label: str, csv_column_name: str):
        """Initialize the transaction source."""
        self.sankey_label: str = sankey_label
        self.csv_column_name: str = csv_column_name
        self.csv_value_filters: list[str] = []

    def to_dict(self) -> dict:
        """Convert the transaction source to a dictionary."""
        return {
            'sankey_label': self.sankey_label,
            'csv_column_name': self.csv_column_name,
            'csv_value_filters': self.csv_value_filters,
        }


class AccountSource:
    """Model for an income source."""

    def __init__(self, account_name: str, iban: str):
        """Initialize the income source."""
        self.account_name: str = account_name
        self.iban: str = iban
        self.income_filters: list[IncomeFilter] = []

    def to_dict(self) -> dict:
        """Convert the income source to a dictionary."""
        return {
            'account_name': self.account_name,
            'iban': self.iban,
            'income_filters': [filter.__dict__ for filter in self.income_filters],
        }


class DataFrameFilter:
    """Model for a DataFrame filter."""

    def __init__(self, csv_column_name: str, csv_value_filters: list[str]):
        """Initialize the DataFrame filter."""
        self.csv_column_name: str = csv_column_name
        self.csv_value_filters: str = csv_value_filters

    def to_dict(self) -> dict:
        """Convert the DataFrame filter to a dictionary."""
        return {
            'csv_column_name': self.csv_column_name,
            'csv_value_filters': self.csv_value_filters,
        }


class IssueCategory:
    """Model for an issue category."""

    def __init__(self, csv_column_name: str):
        """Initialize the issue category."""
        self.csv_column_name: str = csv_column_name
        self.sub_category: IssueCategory = None

    def get_depth(self) -> int:
        """Get the depth of the issue category."""
        if not self.sub_category:
            return 1
        return 1 + self.sub_category.get_depth()

    def to_dict(self) -> dict:
        """Convert the issue category to a dictionary."""
        return {
            'csv_column_name': self.csv_column_name,
            'sub_category': self.sub_category.to_dict() if self.sub_category else None,
        }


class Config:
    """Store the configuration data for the Sankey Generator."""

    def __init__(
        self,
        input_file: str,
        output_file: str,
        income_reference_accounts: list[AccountSource],
        income_data_frame_filters: list[DataFrameFilter],
        issues_data_frame_filters: list[DataFrameFilter],
        issues_hierarchy: IssueCategory,
        income_node_name: str,
        not_used_income_name: str,
        analysis_year_column_name: str,
        analysis_month_column_name: str,
        amount_out_name: str,
        other_income_name: str,
        last_used_month: int,
        last_used_year: int,
        last_used_issue_level: int,
        dark_mode: bool,
    ):
        """Initialize the configuration data."""
        self.input_file: str = input_file
        self.output_file: str = output_file
        self.income_reference_accounts: list[AccountSource] = income_reference_accounts
        self.income_data_frame_filters: list[DataFrameFilter] = income_data_frame_filters
        self.issues_data_frame_filters: list[DataFrameFilter] = issues_data_frame_filters
        self.issues_hierarchy: IssueCategory = issues_hierarchy
        self.income_node_name: str = income_node_name
        self.not_used_income_name: str = not_used_income_name
        self.analysis_year_column_name: str = analysis_year_column_name
        self.analysis_month_column_name: str = analysis_month_column_name
        self.amount_out_name: str = amount_out_name
        self.other_income_name: str = other_income_name
        self.last_used_month: int = last_used_month
        self.last_used_year: int = last_used_year
        self.last_used_issue_level: int = last_used_issue_level
        self.dark_mode: bool = dark_mode

    def to_dict(self) -> dict:
        """Convert the configuration data to a dictionary."""
        return {
            'input_file': self.input_file,
            'output_file': self.output_file,
            'income_reference_accounts': [account.to_dict() for account in self.income_reference_accounts],
            'income_data_frame_filters': [filter.to_dict() for filter in self.income_data_frame_filters],
            'issues_data_frame_filters': [filter.to_dict() for filter in self.issues_data_frame_filters],
            'issues_hierarchy': self.issues_hierarchy.to_dict(),
            'income_node_name': self.income_node_name,
            'not_used_income_name': self.not_used_income_name,
            'analysis_year_column_name': self.analysis_year_column_name,
            'analysis_month_column_name': self.analysis_month_column_name,
            'amount_out_name': self.amount_out_name,
            'other_income_name': self.other_income_name,
            'last_used_month': int(self.last_used_month),
            'last_used_year': int(self.last_used_year),
            'last_used_issue_level': int(self.last_used_issue_level),
            'dark_mode': bool(self.dark_mode),
        }
