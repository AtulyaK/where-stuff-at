"""Sidebar navigation component.

Provides the primary application navigation menu based on design specs.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QCursor
from typing import Dict
import qtawesome as qta


class Sidebar(QWidget):
    """A vertical navigation menu for switching views.

    Attributes:
        navigation_requested: A signal emitted when a navigation button is clicked,
                              passing the string name of the target route.
        nav_buttons: A dictionary tracking button instances by route name.
    """

    navigation_requested = pyqtSignal(str)

    def __init__(self) -> None:
        """Initializes the Sidebar layout and default buttons."""
        super().__init__()
        self.setObjectName("Sidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Where's My Stuff?")
        title.setObjectName("SidebarAppTitle")
        layout.addWidget(title)

        self.nav_buttons: Dict[str, QPushButton] = {}

        nav_items = [
            ("Dashboard", "fa5s.home"),
            ("Add Item", "fa5s.plus"),
            ("Locations", "fa5s.map-marker-alt"),
            ("All Items", "fa5s.list"),
            ("Search", "fa5s.search"),
        ]

        for name, icon_name in nav_items:
            btn = QPushButton(name)
            btn.setObjectName("SidebarButton")
            btn.setIcon(qta.icon(icon_name, color="#737373"))
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setProperty("active", "false")

            # Capture variable dynamically in lambda using default arg
            btn.clicked.connect(
                lambda checked, route=name: self._handle_nav_click(route)
            )

            self.nav_buttons[name] = btn
            layout.addWidget(btn)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        layout.addItem(spacer)

        self.set_active("Dashboard")

    def _handle_nav_click(self, route_name: str) -> None:
        """Processes navigation button clicks.

        Args:
            route_name: The target route name associated with the button.
        """
        self.set_active(route_name)
        self.navigation_requested.emit(route_name)

    def set_active(self, active_route: str) -> None:
        """Updates the visual active state of the sidebar buttons.

        Args:
            active_route: The name of the route currently deemed active.
        """
        for name, btn in self.nav_buttons.items():
            is_active = name == active_route
            property_str = "true" if is_active else "false"
            icon_color = "#ffffff" if is_active else "#737373"

            btn.setProperty("active", property_str)
            btn.setIcon(qta.icon(self._get_icon_for_route(name), color=icon_color))

            # Recompile QSS rules specifically for this button
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def _get_icon_for_route(self, route: str) -> str:
        """Maps route names to qtawesome icon names."""
        icons = {
            "Dashboard": "fa5s.home",
            "Add Item": "fa5s.plus",
            "Locations": "fa5s.map-marker-alt",
            "All Items": "fa5s.list",
            "Search": "fa5s.search",
        }
        return icons.get(route, "fa5s.circle")
