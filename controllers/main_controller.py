"""Main controller logic connecting views and core data models.

Ensures that UI and business logic are fully decoupled. Handles async data
loading and state management using QThread for non-blocking UI interactions.
"""

from PyQt6.QtCore import QObject, pyqtSignal, QThread
from typing import List, Optional
import time

from core.models import Item, Location
from utils.logger import get_logger

logger = get_logger(__name__)


class DataLoadWorker(QThread):
    """A worker thread to simulate asynchronous data loading.

    This ensures that the UI does not block while doing heavy computations
    or database fetches.

    Attributes:
        items_loaded: Signal emitted when items have finished loading.
        locations_loaded: Signal emitted when locations have finished loading.
        error_occurred: Signal emitted if an error happens during load.
    """

    items_loaded = pyqtSignal(list)
    locations_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def run(self) -> None:
        """Executes the data loading simulation off the main thread."""
        logger.info("Starting background data load.")
        try:
            # Simulate network or heavy DB latency
            time.sleep(1.0)

            # Mock Items
            items = [
                Item(
                    id="1",
                    name="MacBook Pro 16",
                    description="M2 Max, 32GB RAM",
                    quantity=12,
                    tags=["Electronics", "Laptop"],
                    icon_name="fa5s.laptop",
                ),
                Item(
                    id="2",
                    name="Sony Alpha a7 III",
                    description="Mirrorless camera body",
                    quantity=1,
                    tags=["Electronics", "Camera"],
                    icon_name="fa5s.camera",
                ),
                Item(
                    id="3",
                    name="Office Chair",
                    description="Herman Miller Aeron",
                    quantity=5,
                    tags=["Furniture"],
                    icon_name="fa5s.chair",
                ),
                Item(
                    id="4",
                    name="Logitech MX Master",
                    description="Wireless Mouse",
                    quantity=3,
                    tags=["Electronics", "Accessories"],
                    icon_name="fa5s.mouse",
                ),
            ]
            self.items_loaded.emit(items)

            # Mock Locations
            locations = [
                Location(id="loc1", name="Office", loc_type="room"),
                Location(id="loc2", name="Garage", loc_type="room"),
            ]
            self.locations_loaded.emit(locations)

            logger.info("Background data load completed successfully.")
        except Exception as e:
            logger.error(f"Error loading dummy data: {e}")
            self.error_occurred.emit(str(e))


class MainController(QObject):
    """The central application controller coordinating models and views.

    Attributes:
        data_updated: Signal emitted whenever the underlying state changes.
        items: The application's current list of items in state.
        locations: The application's current list of locations in state.
    """

    data_updated = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.items: List[Item] = []
        self.locations: List[Location] = []
        self.worker: Optional[DataLoadWorker] = None
        logger.debug("MainController initialized.")

    def load_initial_data(self) -> None:
        """Starts the asynchronous data loading process."""
        logger.info("Triggering data load.")
        self.worker = DataLoadWorker()
        self.worker.items_loaded.connect(self._on_items_loaded)
        self.worker.locations_loaded.connect(self._on_locations_loaded)
        self.worker.error_occurred.connect(self._on_error)
        self.worker.start()

    def _on_items_loaded(self, retrieved_items: List[Item]) -> None:
        """Handler for when items are successfully loaded.

        Args:
            retrieved_items: The newly loaded items from the worker.
        """
        self.items = retrieved_items
        logger.debug(f"Loaded {len(self.items)} items into state.")
        self.data_updated.emit()

    def _on_locations_loaded(self, retrieved_locations: List[Location]) -> None:
        """Handler for when locations are successfully loaded.

        Args:
            retrieved_locations: The newly loaded locations from the worker.
        """
        self.locations = retrieved_locations
        logger.debug(f"Loaded {len(self.locations)} locations into state.")
        self.data_updated.emit()

    def _on_error(self, error_msg: str) -> None:
        """Logs and handles load errors.

        Args:
            error_msg: The string description of the error.
        """
        logger.error(f"Controller received load error: {error_msg}")
        # In MVVM, we'd emit an error signal to the view here to pop a QMessageBox
