"""Search view implementation.

Provides a robust input form with filters and dynamically displays
horizontal SearchResultItems matching the requested queries.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QLineEdit,
    QComboBox,
    QFrame,
)
import qtawesome as qta
from typing import Optional

from gui.components.buttons import PrimaryButton
from utils.logger import get_logger

logger = get_logger(__name__)


class SearchResultItem(QFrame):
    """A horizontally stretched card displaying brief matched item details."""

    def __init__(
        self, name: str, description: str, category: str, icon_name: str = "fa5s.box"
    ) -> None:
        """Initializes the SearchResultItem.

        Args:
            name: The title/name of the item found.
            description: Concise description string.
            category: Classification of the item (e.g. 'Electronics').
            icon_name: Base icon identifier.
        """
        super().__init__()
        self.setProperty("class", "Card")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color="#737373").pixmap(32, 32))

        info_layout = QVBoxLayout()
        title = QLabel(name)
        title.setStyleSheet("font-size: 16px; font-weight: 600;")
        desc = QLabel(description)
        desc.setProperty("class", "TextMuted")

        info_layout.addWidget(title)
        info_layout.addWidget(desc)

        cat_label = QLabel(category)
        cat_label.setStyleSheet("color: #3b82f6; font-size: 14px; font-weight: 500;")

        layout.addWidget(icon)
        layout.addLayout(info_layout, 1)
        layout.addWidget(cat_label)


class SearchView(QWidget):
    """The central widget coordinating user search queries and rendering results."""

    def __init__(self) -> None:
        """Initializes the SearchView layout."""
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QWidget()
        header.setObjectName("HeaderArea")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        title = QLabel("Search Items")
        title.setObjectName("HeaderTitle")
        header_layout.addWidget(title)

        layout.addWidget(header)

        form_widget = QWidget()
        form_layout = QHBoxLayout(form_widget)
        form_layout.setContentsMargins(24, 24, 24, 0)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by name, description, or tags...")

        loc_combo = QComboBox()
        loc_combo.addItems(["All Categories", "Electronics", "Furniture", "Books"])

        search_btn = PrimaryButton("Search", "fa5s.search")
        search_btn.setStyleSheet("padding: 12px 24px; font-size: 16px;")

        form_layout.addWidget(search_input, 3)
        form_layout.addWidget(loc_combo, 1)
        form_layout.addWidget(search_btn)

        layout.addWidget(form_widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent; margin-top: 24px;")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 0, 24, 24)
        content_layout.setSpacing(16)

        # Dummy Results simulating controller injection
        content_layout.addWidget(
            SearchResultItem(
                "MacBook Pro 16",
                "M2 Max, 32GB RAM, Space Gray.",
                "Electronics",
                "fa5s.laptop",
            )
        )
        content_layout.addWidget(
            SearchResultItem(
                "Logitech MX Master",
                "Wireless Ergonomic Mouse.",
                "Electronics",
                "fa5s.mouse",
            )
        )
        content_layout.addWidget(
            SearchResultItem(
                "Keychron K8 Pro",
                "Mechanical Keyboard with brown switches.",
                "Electronics",
                "fa5s.keyboard",
            )
        )

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        logger.debug("SearchView initialized successfully.")
