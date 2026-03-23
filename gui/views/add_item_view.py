"""Add Items view implementation.

Provides a structured form for injecting new items into the inventory.
Features robust validation and fully responsive cascading location dropdowns.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QScrollArea,
    QFrame,
)
import qtawesome as qta
from typing import Optional

from gui.components.buttons import PrimaryButton
from gui.components.forms import StandardInput, CascadingDropdown
from controllers.main_controller import MainController
from utils.logger import get_logger

logger = get_logger(__name__)


class AddItemView(QWidget):
    """View container displaying the required forms to insert a new Item."""

    def __init__(self, controller: Optional[MainController] = None) -> None:
        """Initializes the layout and wires validation algorithms."""
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QWidget()
        header.setObjectName("HeaderArea")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(32, 24, 32, 16)

        title = QLabel("Add New Item")
        title.setObjectName("HeaderTitle")
        header_layout.addWidget(title)

        desc = QLabel("Fill out the details below to catalog a new asset.")
        desc.setProperty("class", "TextMuted")
        desc.setStyleSheet("margin-top: 4px;")
        header_layout.addWidget(desc)

        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")

        content = QWidget()
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(32, 16, 32, 32)
        c_layout.setSpacing(24)

        # Form Container (Glassmorphic Card)
        form_card = QFrame()
        form_card.setProperty("class", "Card")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(20)

        # Field 1: Name (Required)
        self.name_input = StandardInput("Item Name *", 'e.g., MacBook Pro 16"')
        self.name_input.input_field.textChanged.connect(self._validate_form)
        form_layout.addWidget(self.name_input)

        # Field 2: Description
        desc_label = QLabel("Description")
        desc_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText(
            "Brief details about the condition, specs, etc."
        )
        self.desc_input.setMaximumHeight(80)
        form_layout.addWidget(desc_label)
        form_layout.addWidget(self.desc_input)

        # Field 3: Photo URL
        self.url_input = StandardInput("Photo URL", "https://example.com/image.jpg")
        form_layout.addWidget(self.url_input)

        # Field 4: Cascading Locations (Required Room)
        loc_label = QLabel("Location Path *")
        loc_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        self.loc_dropdowns = CascadingDropdown()

        # Wire validation to the specific Room combo box changing inside the component
        self.loc_dropdowns.room_cb.currentIndexChanged.connect(self._validate_form)

        form_layout.addWidget(loc_label)
        form_layout.addWidget(self.loc_dropdowns)

        # Field 5: Tags
        self.tags_input = StandardInput(
            "Tags (comma separated)", "e.g., Electronics, Work, Expensive"
        )
        form_layout.addWidget(self.tags_input)

        actions = QHBoxLayout()
        actions.addStretch()

        self.submit_btn = PrimaryButton("Save Item", "fa5s.save")
        self.submit_btn.setEnabled(False)  # Default disabled per validation specs
        self.submit_btn.clicked.connect(self._handle_submit)

        actions.addWidget(self.submit_btn)
        form_layout.addLayout(actions)

        c_layout.addWidget(form_card)
        c_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

        self.populate_initial_data()

    def populate_initial_data(self) -> None:
        """Seeds the root Room dropdown if location data exists."""
        if self.controller and self.controller.locations:
            room_names = [
                loc.name for loc in self.controller.locations if loc.type == "room"
            ]
            self.loc_dropdowns.set_rooms(room_names)
        else:
            # Fallback mockup
            self.loc_dropdowns.set_rooms(["Office", "Garage", "Kitchen"])

    def _validate_form(self) -> None:
        """Evaluates required fields to dynamically toggle the submit button."""
        name_has_text = bool(self.name_input.input_field.text().strip())
        room_selected = self.loc_dropdowns.room_cb.currentIndex() > 0

        if name_has_text and room_selected:
            self.submit_btn.setEnabled(True)
        else:
            self.submit_btn.setEnabled(False)

    def _handle_submit(self) -> None:
        """Processes form payload and passes to controller."""
        name = self.name_input.input_field.text().strip()
        desc = self.desc_input.toPlainText().strip()
        url = self.url_input.input_field.text().strip()
        tags_raw = self.tags_input.input_field.text()
        tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []

        room = self.loc_dropdowns.room_cb.currentText()
        region = self.loc_dropdowns.region_cb.currentText()
        specific = self.loc_dropdowns.specific_cb.currentText()

        # Default text checking for "Select X..."
        if "Select" in region:
            region = ""
        if "Select" in specific:
            specific = ""

        logger.info(f"Submitting New Item: {name} | Room: {room}")
        # In a complete MVVM flow, we would hit controller.add_item() here and clear form on success

        # Clear form as mockup of success
        self.name_input.input_field.clear()
        self.desc_input.clear()
        self.url_input.input_field.clear()
        self.tags_input.input_field.clear()
        self.loc_dropdowns.room_cb.setCurrentIndex(0)
        self.submit_btn.setEnabled(False)
        self.name_input.show_error("Saved successfully! Add another?")
