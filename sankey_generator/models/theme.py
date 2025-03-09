"""Color theme for the application."""


class Theme:
    """Color theme for the application."""

    dark_mode = True

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
        'primary': '#1976d2',
        'secondary': '#26a69a',
        'accent': '#e91e63',
        'background': '#ffffff',
        'page': '#f5f5f5',
        'positive': '#4caf50',
        'negative': '#f44336',
        'info': '#2196f3',
        'warning': '#ff9800',
    }

    @classmethod
    def get_colors(cls):
        return cls.dark if cls.dark_mode else cls.light

    @classmethod
    def toggle_mode(cls):
        cls.dark_mode = not cls.dark_mode
