"""Form components including strict inputs and cascading dropdowns.

Provides styled replacements for QLineEdit and QComboBoxes to match
the Tailwind design specifications and handle dynamic validation.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
)
from typing import List

from utils.logger import get_logger

logger = get_logger(__name__)


class StandardInput(QWidget):
    """A styled text input widget with integrated dynamic error messaging."""

    def __init__(self, label_text: str, placeholder: str = "") -> None:
        """Initializes the standard input.

        Args:
            label_text: The label displayed above the text input.
            placeholder: Placeholder text inside the input box.
        """
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label_text)
        self.label.setStyleSheet("font-size: 14px; font-weight: 500;")
        layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(placeholder)
        layout.addWidget(self.input_field)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ef4444; font-size: 12px;")
        self.error_label.hide()
        layout.addWidget(self.error_label)

    def show_error(self, message: str) -> None:
        """Displays an error string below the input and turns borders red."""
        self.error_label.setText(message)
        self.error_label.show()
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ef4444;
            }
        """)
        logger.debug(f"Input validation error shown: {message}")

    def clear_error(self) -> None:
        """Hides any active error state and resets border colors."""
        self.error_label.hide()
        self.input_field.setStyleSheet("")


class CascadingDropdown(QWidget):
    """A series of dropdowns simulating a Room > Region > Specific nested flow.

    The state of child dropdowns resets dynamically based on parent selections.
    """

    def __init__(self) -> None:
        """Initializes the cascading hierarchy layout and connects signals."""
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        combo_style = """
            QComboBox {
                min-width: 150px;
            }
            QComboBox:disabled {
                background-color: rgba(255, 255, 255, 0.05);
                color: #475569;
                border: 1px solid #1e293b;
            }
        """

        self.room_cb = QComboBox()
        self.room_cb.setStyleSheet(combo_style)
        self.room_cb.addItem("Select Room...")

        self.region_cb = QComboBox()
        self.region_cb.setStyleSheet(combo_style)
        self.region_cb.addItem("Select Region...")
        self.region_cb.setEnabled(False)

        self.specific_cb = QComboBox()
        self.specific_cb.setStyleSheet(combo_style)
        self.specific_cb.addItem("Select Specific...")
        self.specific_cb.setEnabled(False)

        layout.addWidget(self.room_cb)
        layout.addWidget(self.region_cb)
        layout.addWidget(self.specific_cb)

        self.room_cb.currentIndexChanged.connect(self._on_room_changed)
        self.region_cb.currentIndexChanged.connect(self._on_region_changed)

    def set_rooms(self, rooms: List[str]) -> None:
        """Populates the root Room dropdown.

        Args:
            rooms: A list of string location names.
        """
        self.room_cb.clear()
        self.room_cb.addItem("Select Room...")
        self.room_cb.addItems(rooms)

    def _on_room_changed(self, index: int) -> None:
        """Handles resetting and populating Region based on Room selection."""
        if index > 0:
            self.region_cb.setEnabled(True)
            self.region_cb.clear()
            self.region_cb.addItem("Select Region...")

            # Logic would ordinarily hit the controller here.
            room_name = self.room_cb.currentText()
            self.region_cb.addItems([f"{room_name} Top", f"{room_name} Bottom"])
        else:
            self.region_cb.setEnabled(False)
            self.region_cb.setCurrentIndex(0)
            self.specific_cb.setEnabled(False)
            self.specific_cb.setCurrentIndex(0)

    def _on_region_changed(self, index: int) -> None:
        """Handles resetting and populating Specific based on Region selection."""
        if index > 0:
            self.specific_cb.setEnabled(True)
            self.specific_cb.clear()
            self.specific_cb.addItem("Select Specific...")
            region = self.region_cb.currentText()
            self.specific_cb.addItems([f"{region} Bin 1", f"{region} Bin 2"])
        else:
            self.specific_cb.setEnabled(False)
            self.specific_cb.setCurrentIndex(0)
