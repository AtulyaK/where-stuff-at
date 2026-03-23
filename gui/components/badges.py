"""Custom Badge widget.

Provides small, pill-shaped informational labels for tags and statuses.
"""

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


class Badge(QLabel):
    """A visual badge component representing categorization tags.

    Designed to map to a secondary badge variant (light green background,
    dark green text, fully rounded edges).
    """

    def __init__(self, text: str) -> None:
        """Initializes the Badge widget.

        Args:
            text: The string literal to display inside the badge.
        """
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #eff6ff;
                color: #1d4ed8;
                border-radius: 12px;
                padding: 4px 10px;
                font-size: 12px;
                font-weight: 500;
            }
        """)
