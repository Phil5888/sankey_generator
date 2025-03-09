"""Color theme for the application."""


class Theme:
    """Color theme for the application."""

    dark = {
        'primary': '#5898d4',
        'secondary': '#26a69a',
        'accent': '#9c27b0',
        'background': '#1d1d1d',
        'page': '#121212',
        'positive': '#21ba45',
        'negative': '#c10015',
        'info': '#31ccec',
        'warning': '#f2c037',
    }

    light = {
        'primary': '#1565c0',
        'secondary': '#26a69a',
        'accent': '#d81b60',
        'background': '#f5f5f5',
        'page': '#e0e0e0',
        'positive': '#4caf50',
        'negative': '#e53935',
        'info': '#1e88e5',
        'warning': '#fb8c00',
    }

    dark_mode = True

    @staticmethod
    def get_colors() -> dict:
        """Get the colors for the current theme."""
        return Theme.dark if Theme.dark_mode else Theme.light

    @staticmethod
    def toggle_mode() -> None:
        """Toggle the theme mode between dark and light."""
        Theme.dark_mode = not Theme.dark_mode
