from sankey_generator.models.config import Config
from sankey_generator.services.config_service import ConfigService
from sankey_generator.utils.observer import Observable, ObserverKeys
from sankey_generator.models.config import AccountSource, DataFrameFilter


class ConfigController(Observable):
    """Controller for the configuration window."""

    def __init__(self, config_service: ConfigService):
        """Initialize the configuration controller."""
        super().__init__()
        self.config_service: ConfigService = config_service
        config: Config = config_service.config
        # TODO: Work with copies here to avoid modifying the original config until save
        self.income_reference_accounts: list[AccountSource] = config.income_reference_accounts
        self.issues_data_frame_filters: list[DataFrameFilter] = config.issues_data_frame_filters
        self.income_data_frame_filters: list[DataFrameFilter] = config.income_data_frame_filters

    def save_config(self):
        """Save changes to the config."""
        # TBD: Validate the config before saving

        self.config_service._save_config()
        self.notify_observers(ObserverKeys.INFO_MESSAGE, 'Configuration saved successfully.')
        self.notify_observers(ObserverKeys.CLOSE_WINDOW)

    def add_issues_filter(self, filter: str):
        """Add a new issues filter."""
        self.issues_data_frame_filters.append(filter)
        self.notify_observers(ObserverKeys.ISSUES_FITLERS_CHANGED)

    def edit_issues_filter(self, index: int, new_filter: str):
        """Edit an existing issues filter."""
        if 0 <= index < len(self.issues_data_frame_filters):
            self.issues_data_frame_filters[index] = new_filter
            self.notify_observers(ObserverKeys.ISSUES_FITLERS_CHANGED)
        else:
            self.notify_observers(ObserverKeys.ERROR_MESSAGE, 'Invalid index for issues filter.')

    def delete_issues_filter(self, index: int):
        """Delete an existing issues filter."""
        if 0 <= index < len(self.issues_data_frame_filters):
            del self.issues_data_frame_filters[index]
            self.notify_observers(ObserverKeys.ISSUES_FITLERS_CHANGED)
        else:
            self.notify_observers(ObserverKeys.ERROR_MESSAGE, 'Invalid index for issues filter.')

    def add_income_filter(self, filter: str):
        """Add a new income filter."""
        self.income_data_frame_filters.append(filter)
        self.notify_observers(ObserverKeys.INCOME_FITLERS_CHANGED)

    def edit_income_filter(self, index: int, new_filter: str):
        """Edit an existing income filter."""
        if 0 <= index < len(self.income_data_frame_filters):
            self.income_data_frame_filters[index] = new_filter
            self.notify_observers(ObserverKeys.INCOME_FITLERS_CHANGED)
        else:
            self.notify_observers(ObserverKeys.ERROR_MESSAGE, 'Invalid index for income filter.')

    def delete_income_filter(self, index: int):
        """Delete an existing income filter."""
        if 0 <= index < len(self.income_data_frame_filters):
            del self.income_data_frame_filters[index]
            self.notify_observers(ObserverKeys.INCOME_FITLERS_CHANGED)
        else:
            self.notify_observers(ObserverKeys.ERROR_MESSAGE, 'Invalid index for income filter.')

    def add_income_reference_account(self, account: AccountSource):
        """Add a new income reference account."""
        self.income_reference_accounts.append(account)
        self.notify_observers(ObserverKeys.INCOME_REFERENCE_ACCOUNTS_CHANGED)

    def delete_income_reference_account(self, index: int):
        """Delete an existing income reference account."""
        if 0 <= index < len(self.income_reference_accounts):
            del self.income_reference_accounts[index]
            self.notify_observers(ObserverKeys.INCOME_REFERENCE_ACCOUNTS_CHANGED)
        else:
            self.notify_observers(ObserverKeys.ERROR_MESSAGE, 'Invalid index for income reference account.')

    def edit_income_reference_account(self, index: int, account: AccountSource):
        """Edit an existing income reference account."""
        if 0 <= index < len(self.income_reference_accounts):
            self.income_reference_accounts[index] = account
            self.notify_observers(ObserverKeys.INCOME_REFERENCE_ACCOUNTS_CHANGED)
        else:
            self.notify_observers(ObserverKeys.ERROR_MESSAGE, 'Invalid index for income reference account.')
