"""Theme manager for handling theme-related logic and applying themes to the application."""

from sankey_generator.models.theme import Theme
from sankey_generator.services.config_service import ConfigService


class ThemeService:
    """Manager for handling theme-related logic."""

    def __init__(self, config_service):
        """Initialize the theme manager."""
        self.config_service: ConfigService = config_service

    def get_stylesheet(self) -> str:
        """Apply the current theme to the given window."""
        colors = Theme.get_colors()
        with open('sankey_generator/resources/theme.qss', 'r') as file:
            stylesheet = file.read().format(**colors)
        return stylesheet

    def get_colors(self) -> dict:
        """Get the current theme colors."""
        return Theme.get_colors()

    def toggle_theme(self):
        """Toggle the theme and save the preference."""
        Theme.toggle_mode()
        self.config_service.save_dark_mode(Theme.dark_mode)
