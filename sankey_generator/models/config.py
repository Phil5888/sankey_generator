"""Store the configuration data for the Sankey Generator."""


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
        self.income_filters: list[IncomeFilter] = []


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

    def get_depth(self) -> int:
        """Get the depth of the issue category."""
        if not self.sub_category:
            return 1
        return 1 + self.sub_category.get_depth()


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
