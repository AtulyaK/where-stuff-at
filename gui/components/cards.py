"""Card widgets for dashboard analytics and item displays.

These components implement the visual "Card" styling featuring
subtle borders, drop shadows (simulated), and content padding.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from typing import Optional, List
import qtawesome as qta

from gui.components.badges import Badge


class StatsCard(QFrame):
    """A card used to display a single, high-impact statistic.

    Typically used in dashboards for metrics like 'Total Items'.
    """

    def __init__(
        self, title: str, value_str: str, icon_name: str = "fa5s.chart-bar"
    ) -> None:
        """Initializes the StatsCard.

        Args:
            title: The descriptive label of the statistic.
            value_str: The formatted string value to display.
            icon_name: An optional qtawesome icon describing the stat.
        """
        super().__init__()
        self.setObjectName("StatsCard")
        self.setProperty("class", "Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        header_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setObjectName("StatsCardTitle")

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color="#94a3b8").pixmap(16, 16))

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(icon_label)

        value_label = QLabel(value_str)
        value_label.setObjectName("StatsCardValue")

        layout.addLayout(header_layout)
        layout.addWidget(value_label)


class RecentItemRow(QFrame):
    """A horizontal row displaying a single recent item in the Dashboard.

    Contains the thumbnail, name, description, and nested location path.
    """

    def __init__(
        self,
        name: str,
        description: str,
        location_path: str,
        icon_name: str = "fa5s.box",
    ) -> None:
        """Initializes the RecentItemRow.

        Args:
            name: The name of the item.
            description: Short description of the item.
            location_path: Formatted string like "Office > Desk Area".
            icon_name: Icon for thumbnail fallback.
        """
        super().__init__()
        self.setProperty("class", "Card")
        # Overriding card background to slightly flat row approach
        self.setStyleSheet(
            "QFrame { background-color: rgba(255,255,255,0.02); border-radius: 8px; margin-bottom: 8px; } QFrame:hover { background-color: rgba(255,255,255,0.06); }"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        # Thumbnail
        thumb_bg = QWidget()
        thumb_bg.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 6px;")
        thumb_bg.setFixedSize(48, 48)
        thumb_layout = QVBoxLayout(thumb_bg)
        thumb_layout.setContentsMargins(0, 0, 0, 0)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(qta.icon(icon_name, color="#94a3b8").pixmap(24, 24))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumb_layout.addWidget(icon_lbl)

        # Info Columns
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(12, 0, 0, 0)
        info_layout.setSpacing(4)

        title_lbl = QLabel(name)
        title_lbl.setProperty("class", "TextCardTitle")

        desc_lbl = QLabel(description)
        desc_lbl.setProperty("class", "TextMuted")

        info_layout.addWidget(title_lbl)
        info_layout.addWidget(desc_lbl)

        # Location Path (Right aligned)
        loc_layout = QVBoxLayout()
        loc_lbl = QLabel(location_path)
        loc_lbl.setStyleSheet("color: #22c55e; font-size: 13px; font-weight: 500;")
        loc_lbl.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        loc_layout.addWidget(loc_lbl)

        layout.addWidget(thumb_bg)
        layout.addLayout(info_layout, 1)
        layout.addLayout(loc_layout)


class ItemCard(QFrame):
    """A card used to display an individual inventory item's details.

    Contains a placeholder area for an image/icon, the item title,
    a truncated description, tags, and standard metadata.
    """

    def __init__(
        self,
        item_name: str,
        description: str,
        tags: Optional[List[str]] = None,
        date_str: str = "",
        icon_name: str = "fa5s.box",
    ) -> None:
        """Initializes the ItemCard.

        Args:
            item_name: The title/name of the inventory item.
            description: A short text description.
            tags: A list of string tags to render as Badges.
            date_str: A formatted string showing when the item was added or updated.
            icon_name: The fallback qtawesome icon to show in place of an image.
        """
        super().__init__()
        self.setProperty("class", "Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        img_placeholder = QWidget()
        img_placeholder.setStyleSheet(
            "background-color: rgba(0,0,0,0.3); border-top-left-radius: 12px; border-top-right-radius: 12px;"
        )
        img_placeholder.setMinimumHeight(140)
        img_layout = QVBoxLayout(img_placeholder)
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color="#475569").pixmap(48, 48))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_layout.addWidget(icon_label)

        layout.addWidget(img_placeholder)

        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(16, 16, 16, 16)

        title = QLabel(item_name)
        title.setObjectName("ItemCardTitle")
        title.setProperty("class", "TextCardTitle")
        details_layout.addWidget(title)

        desc = QLabel(description)
        desc.setObjectName("ItemCardDescription")
        desc.setProperty("class", "TextMuted")
        desc.setWordWrap(True)
        desc.setMaximumHeight(40)
        details_layout.addWidget(desc)

        if tags:
            tags_layout = QHBoxLayout()
            tags_layout.setSpacing(8)
            for tag in tags:
                tags_layout.addWidget(Badge(tag))
            tags_layout.addStretch()
            details_layout.addLayout(tags_layout)

        if date_str:
            date_layout = QHBoxLayout()
            clock_icon = QLabel()
            clock_icon.setPixmap(qta.icon("fa5s.clock", color="#94a3b8").pixmap(14, 14))
            date_label = QLabel(date_str)
            date_label.setProperty("class", "TextMuted")
            date_layout.addWidget(clock_icon)
            date_layout.addWidget(date_label)
            date_layout.addStretch()
            details_layout.addLayout(date_layout)

        layout.addWidget(details_widget)
