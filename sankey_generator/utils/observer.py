"""Implementation for observer pattern."""


class Observable:
    """Observable class to be used as a base class for any observable object."""

    def __init__(self):
        """Initialize the observable with an empty list of observers."""
        self.observers: list[Observer] = []

    def add_observer(self, observer):
        """Add an observer to the list of observers."""
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        """Remove an observer from the list of observers."""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        """Notify all observers about an event."""
        for observer in self.observers:
            observer.update(self, *args, **kwargs)


class Observer:
    """Observer class to be used as a base class for any observer object."""

    def update(self, observable, *args, **kwargs):
        """Update method to be implemented by concrete observers."""
        pass
