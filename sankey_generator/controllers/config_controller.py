from sankey_generator.models.config import Config
from sankey_generator.services.config_service import ConfigService
from sankey_generator.utils.observer import Observable, ObserverKeys


class ConfigController(Observable):
    """Controller for the configuration window."""

    def __init__(self, config_service: ConfigService):
        """Initialize the configuration controller."""
        super().__init__()
        self.config_service: ConfigService = config_service
        config: Config = config_service.config
        # TODO: Work with copies here to avoid modifying the original config until save
        self.income_reference_accounts: list = config.income_reference_accounts
        self.issues_data_frame_filters: list = config.issues_data_frame_filters
        self.income_data_frame_filters: list = config.income_data_frame_filters

    def save_config(self):
        """Save changes to the config."""
        # TBD: Validate the config before saving

        self.config_service._save_config()
        self.notify_observers(ObserverKeys.INFO_MESSAGE, 'Configuration saved successfully.')
        self.notify_observers(ObserverKeys.CLOSE_WINDOW)
