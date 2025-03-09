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
        'primary': '#1565c0',  # Slightly darker blue for less brightness
        'secondary': '#26a69a',
        'accent': '#d81b60',  # Softer pink accent
        'background': '#f5f5f5',  # Soft light grey to reduce eye strain
        'page': '#e0e0e0',  # Slightly darker for subtle contrast
        'positive': '#4caf50',
        'negative': '#e53935',  # Slightly toned-down red
        'info': '#1e88e5',  # Less vibrant but clear blue
        'warning': '#fb8c00',  # Muted orange for a softer warning tone
    }

    dark_mode = True  # Default theme mode

    @staticmethod
    def get_colors():
        """Get the current theme colors."""
        return Theme.dark if Theme.dark_mode else Theme.light

    @staticmethod
    def toggle_mode():
        """Toggle the theme mode between dark and light."""
        Theme.dark_mode = not Theme.dark_mode
