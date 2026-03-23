"""All Items view implementation.

Provides a responsive grid displaying a comprehensive list of all
inventory items, filtering bars, and sorting options.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QGridLayout,
    QComboBox,
    QLineEdit,
)
from PyQt6.QtCore import Qt

from gui.components.cards import ItemCard
from utils.logger import get_logger

logger = get_logger(__name__)


class AllItemsView(QWidget):
    """View container for displaying the entire inventory in a grid."""

    def __init__(self) -> None:
        """Initializes the AllItemsView and its grid layouts."""
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header Area
        header = QWidget()
        header.setObjectName("HeaderArea")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)

        title = QLabel("All Items")
        title.setObjectName("HeaderTitle")
        header_layout.addWidget(title)

        # Filters Bar
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(16)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Filter items...")

        loc_combo = QComboBox()
        loc_combo.addItems(["All Locations", "Living Room", "Garage", "Office"])

        sort_combo = QComboBox()
        sort_combo.addItems(["Newest First", "Oldest First", "Name A-Z", "Name Z-A"])

        filters_layout.addWidget(search_input, 2)
        filters_layout.addWidget(loc_combo, 1)
        filters_layout.addWidget(sort_combo, 1)

        header_layout.addLayout(filters_layout)
        layout.addWidget(header)

        # Grid Content Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(24)

        # Standard dummy data fallback if no controller populates it
        dummy_items = [
            (
                "MacBook Pro 16",
                "M2 Max, 32GB RAM",
                ["Electronics"],
                "1 day ago",
                "fa5s.laptop",
            ),
            (
                "Sony Alpha a7 III",
                "Mirrorless camera body",
                ["Electronics"],
                "2 hours ago",
                "fa5s.camera",
            ),
            (
                "Office Chair",
                "Herman Miller Aeron",
                ["Furniture"],
                "3 days ago",
                "fa5s.chair",
            ),
            (
                "Logitech MX Master",
                "Wireless Mouse",
                ["Electronics"],
                "4 days ago",
                "fa5s.mouse",
            ),
            (
                "Keychron K8 Pro",
                "Mechanical Keyboard",
                ["Electronics"],
                "1 week ago",
                "fa5s.keyboard",
            ),
            (
                "Backpack",
                "Peak Design Everyday 20L",
                ["Bags"],
                "2 weeks ago",
                "fa5s.briefcase",
            ),
            (
                "Coffee Maker",
                "Breville Barista Express",
                ["Kitchen"],
                "1 month ago",
                "fa5s.coffee",
            ),
        ]

        row, col = 0, 0
        cols_per_row = 3

        for name, desc, tags, date, icon in dummy_items:
            card = ItemCard(name, desc, tags, date, icon)
            card.setMinimumWidth(280)
            card.setMaximumWidth(400)
            grid_layout.addWidget(card, row, col)

            col += 1
            if col >= cols_per_row:
                col = 0
                row += 1

        content_layout.addLayout(grid_layout)
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        logger.debug("AllItemsView initialized successfully.")
