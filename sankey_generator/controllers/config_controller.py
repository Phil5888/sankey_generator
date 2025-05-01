from sankey_generator.models.config import Config
from sankey_generator.services.config_service import ConfigService
from sankey_generator.utils.observer import Observable


class ConfigController(Observable):
    """Controller for the configuration window."""

    def __init__(self, config_service: ConfigService):
        """Initialize the configuration controller."""
        self.config_service: ConfigService = config_service
        config: Config = config_service.config
        self.issues_reference_accounts: list = config.issues_data_frame_filters
        self.income_data_frame_filters: list = config.income_data_frame_filters
