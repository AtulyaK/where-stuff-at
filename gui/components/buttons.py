"""Custom button widgets.

Provides Primary, Outline, and Destructive button variants tailored to
the application's color scheme and Tailwind styling rules.
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from typing import Optional
import qtawesome as qta


class PrimaryButton(QPushButton):
    """A standard primary action button with a solid green background."""

    def __init__(self, text: str, icon_name: Optional[str] = None) -> None:
        """Initializes the PrimaryButton.

        Args:
            text: The text label to display on the button.
            icon_name: An optional qtawesome icon string (e.g., 'fa5s.plus').
        """
        super().__init__(text)
        self.setObjectName("PrimaryButton")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if icon_name:
            self.setIcon(qta.icon(icon_name, color="white"))


class OutlineButton(QPushButton):
    """A secondary action button with a transparent background and gray outline."""

    def __init__(self, text: str, icon_name: Optional[str] = None) -> None:
        """Initializes the OutlineButton.

        Args:
            text: The text label to display on the button.
            icon_name: An optional qtawesome icon string.
        """
        super().__init__(text)
        self.setObjectName("OutlineButton")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if icon_name:
            self.setIcon(qta.icon(icon_name, color="#0a0a0a"))


class DestructiveButton(QPushButton):
    """A destructive action button with a solid red background."""

    def __init__(self, text: str, icon_name: Optional[str] = None) -> None:
        """Initializes the DestructiveButton.

        Args:
            text: The text label to display on the button.
            icon_name: An optional qtawesome icon string.
        """
        super().__init__(text)
        self.setObjectName("DestructiveButton")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if icon_name:
            self.setIcon(qta.icon(icon_name, color="white"))
