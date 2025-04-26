"""Animated Toggle Switch. Copied from https://www.pythonguis.com/tutorials/pyqt6-animated-widgets/ and modified."""

from PyQt6.QtCore import (
    Qt,
    QSize,
    QPoint,
    QPointF,
    QRectF,
    QEasingCurve,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    pyqtSlot,
    pyqtProperty,
)

from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
from sankey_generator.models.theme import Theme


class AnimatedToggle(QCheckBox):
    """Animated Toggle Switch."""

    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _light_grey_pen = QPen(Qt.GlobalColor.lightGray)

    def __init__(self, parent=None):
        """Initialize the AnimatedToggle."""
        super().__init__(parent)
        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0
        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b'handle_position', self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)

        self.pulse_anim = QPropertyAnimation(self, b'pulse_radius', self)
        self.pulse_anim.setDuration(350)
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

        # Apply initial colors from the current theme
        self.update_colors()

    def update_colors(self):
        """Update colors dynamically from the current theme."""
        colors = Theme.get_colors()
        self._bar_brush = QBrush(QColor(colors['secondary']))
        self._bar_checked_brush = QBrush(QColor(colors['primary']).lighter(110))

        self._handle_brush = QBrush(QColor(colors['page']))
        self._handle_checked_brush = QBrush(QColor(colors['primary']))

        self._pulse_unchecked_animation = QBrush(QColor(colors['secondary'] + '44'))
        self._pulse_checked_animation = QBrush(QColor(colors['primary'] + '44'))

        self.update()

    def paintEvent(self, e: QPaintEvent):
        """Paint the widget."""
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(0, 0, contRect.width() - handleRadius, 0.40 * contRect.height())
        barRect.moveCenter(QPointF(contRect.center()))
        rounding = barRect.height() / 2

        # Handle animation
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.State.Running:
            p.setBrush(self._pulse_checked_animation if self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()), self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)
        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(QPointF(xPos, barRect.center().y()), handleRadius, handleRadius)
        p.end()

    def sizeHint(self):
        """Return the size hint for the widget."""
        return QSize(58, 45)

    def hitButton(self, pos: QPoint):
        """Check if the button was clicked."""
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)
    def setup_animation(self, value):
        """Set default start and end value."""
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    @pyqtProperty(float)
    def handle_position(self):
        """Get the handle position."""
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """
        Summary: Change the handle position.

        Description:
        Change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    @pyqtProperty(float)
    def pulse_radius(self):
        """Get the pulse radius."""
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        """Change the property."""
        self._pulse_radius = pos
        self.update()
