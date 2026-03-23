"""Main Window container and router.

Holds the sidebar and the central stacked widget responsible for routing
between different views in the application.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
)
from typing import Optional
from gui.components.sidebar import Sidebar
from gui.views.dashboard_view import DashboardView
from gui.views.add_item_view import AddItemView
from gui.views.all_items_view import AllItemsView
from gui.views.locations_view import LocationsView
from gui.views.search_view import SearchView

from controllers.main_controller import MainController
from utils.logger import get_logger

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """The main application window.

    Attributes:
        controller: A reference to the MainController managing application state.
        sidebar: The left-side navigation widget.
        stacked_widget: A widget container handling view routing.
    """

    def __init__(self, controller: MainController) -> None:
        """Initializes the main window and its child components.

        Args:
            controller: The central controller managing business logic.
        """
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Where's My Stuff?")
        logger.debug("MainWindow initialized.")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Initialize Sub-Views. Pass controller to views that need data access.
        self.dashboard_view = DashboardView(self.controller)
        self.add_item_view = AddItemView(self.controller)
        self.all_items_view = AllItemsView()
        self.locations_view = LocationsView()
        self.search_view = SearchView()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.add_item_view)
        self.stacked_widget.addWidget(self.all_items_view)
        self.stacked_widget.addWidget(self.locations_view)
        self.stacked_widget.addWidget(self.search_view)

        self.sidebar = Sidebar()
        self.sidebar.navigation_requested.connect(self.navigate)

        content_container = QWidget()
        content_container.setObjectName("MainContent")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.stacked_widget)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_container)

    def navigate(self, route_name: str) -> None:
        """Switches the visible widget in the main application area.

        Args:
            route_name: The name of the route to display (e.g., 'Dashboard').
        """
        pages = {
            "Dashboard": 0,
            "Add Item": 1,
            "All Items": 2,
            "Locations": 3,
            "Search": 4,
        }
        idx = pages.get(route_name, 0)
        self.stacked_widget.setCurrentIndex(idx)
        logger.debug(f"Navigated to: {route_name}")
