"""Locations view representing the nested inventory hierarchy.

It dynamically visualizes Room -> Region -> Specific locations using
nested indentation visual cues.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QToolButton,
)
import qtawesome as qta
from typing import Optional

from gui.components.buttons import OutlineButton, DestructiveButton
from gui.components.badges import Badge
from utils.logger import get_logger

logger = get_logger(__name__)


class LocationBox(QFrame):
    """An overarching widget displaying info and actions for a specific location.

    Attributes:
        indent_level: Specifies how far the box should be indented to represent
                      depth in the hierarchy (e.g., Room=0, Region=1).
    """

    def __init__(
        self,
        name: str,
        loc_type: str,
        item_count: int,
        indent_level: int,
        icon_name: str = "fa5s.map-marker-alt",
        is_expandable: bool = False,
    ) -> None:
        """Initializes the LocationBox.

        Args:
            name: Display name of the location.
            loc_type: String representation of its type (e.g. 'room').
            item_count: Mocked integer of items currently inside.
            indent_level: Integer hierarchy depth multiplier.
            icon_name: Optional qtawesome icon to describe the location type.
            is_expandable: Whether this box can be toggled to show children.
        """
        super().__init__()
        self.setProperty("class", "Card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        margin_left = indent_level * 32
        self.setStyleSheet(f"""
            QFrame {{
                border-radius: 8px;
                margin-left: {margin_left}px;
                margin-bottom: 8px;
            }}
        """)

        content = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color="#3b82f6").pixmap(20, 20))

        info_layout = QVBoxLayout()
        title_row = QHBoxLayout()
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 16px; font-weight: 600;")

        badge = Badge(loc_type.capitalize())

        title_row.addWidget(name_label)
        title_row.addWidget(badge)
        title_row.addStretch()

        desc = QLabel(f"{item_count} items")
        desc.setProperty("class", "TextMuted")

        info_layout.addLayout(title_row)
        info_layout.addWidget(desc)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        
        self.toggle_btn = None
        if is_expandable:
            self.toggle_btn = QToolButton()
            self.toggle_btn.setIcon(qta.icon("fa5s.chevron-down", color="#ffffff"))
            self.toggle_btn.setStyleSheet("border: none; background: transparent;")
            actions.addWidget(self.toggle_btn)
            
        edit_btn = OutlineButton("Edit", "fa5s.edit")
        del_btn = DestructiveButton("Delete", "fa5s.trash-alt")

        edit_btn.setStyleSheet(
            "padding: 4px 8px; border-radius: 4px; font-size: 12px; background:transparent; border:1px solid #e5e5e5;"
        )
        del_btn.setStyleSheet(
            "padding: 4px 8px; border-radius: 4px; font-size: 12px; background:#ef4444; color:white; border:none;"
        )

        actions.addWidget(edit_btn)
        actions.addWidget(del_btn)

        content.addWidget(icon)
        content.addLayout(info_layout, 1)
        content.addLayout(actions)

        layout.addLayout(content)


class AccordionGroup(QWidget):
    """A composite widget wrapping a parent LocationBox and its children."""

    def __init__(self, parent_box: LocationBox, children_boxes: list[QWidget]) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.parent_box = parent_box
        layout.addWidget(self.parent_box)

        self.child_container = QWidget()
        child_layout = QVBoxLayout(self.child_container)
        child_layout.setContentsMargins(0, 0, 0, 0)
        child_layout.setSpacing(0)
        for child in children_boxes:
            child_layout.addWidget(child)

        layout.addWidget(self.child_container)

        self.is_expanded = True
        if self.parent_box.toggle_btn:
            self.parent_box.toggle_btn.clicked.connect(self.toggle)

    def toggle(self) -> None:
        """Toggles the visibility of the children container."""
        self.is_expanded = not self.is_expanded
        self.child_container.setVisible(self.is_expanded)
        icon_name = "fa5s.chevron-down" if self.is_expanded else "fa5s.chevron-right"
        if self.parent_box.toggle_btn:
            self.parent_box.toggle_btn.setIcon(qta.icon(icon_name, color="#ffffff"))


class LocationsView(QWidget):
    """The central view displaying all stored locations in relative hierarchy."""

    def __init__(self) -> None:
        """Initializes the LocationsView and injects dummy data layout."""
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QWidget()
        header.setObjectName("HeaderArea")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        title = QLabel("Locations")
        title.setObjectName("HeaderTitle")
        header_layout.addWidget(title)

        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)

        # Static Dummy Hierarchy simulating MVVM state injection with Accordions
        # Office Group
        office_box = LocationBox("Office", "Room", 120, 0, "fa5s.building", is_expandable=True)
        office_children = [
            LocationBox("Desk Area", "Region", 45, 1, "fa5s.layer-group"),
            LocationBox("Top Drawer", "Specific", 15, 2, "fa5s.archive"),
            LocationBox("Bottom Drawer", "Specific", 30, 2, "fa5s.archive"),
            LocationBox("Bookshelf", "Region", 75, 1, "fa5s.layer-group")
        ]
        content_layout.addWidget(AccordionGroup(office_box, office_children))

        # Garage Group
        garage_box = LocationBox("Garage", "Room", 300, 0, "fa5s.warehouse", is_expandable=True)
        garage_children = [
            LocationBox("Tool Bench", "Region", 50, 1, "fa5s.layer-group"),
            LocationBox("Top Shelf", "Specific", 20, 2, "fa5s.archive")
        ]
        content_layout.addWidget(AccordionGroup(garage_box, garage_children))

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        logger.debug("LocationsView initialized successfully.")
