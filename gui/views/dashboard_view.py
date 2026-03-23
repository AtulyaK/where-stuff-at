"""Dashboard view implementation.

Provides the primary analytics summary and quick access to recent items,
wiring dynamically to the MainController to stay responsive. Incorporates
a collapsible right-side split pane for Data Table analysis.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLabel,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QToolButton,
)
from PyQt6.QtCore import Qt
from typing import Optional

from gui.components.cards import StatsCard, RecentItemRow
from controllers.main_controller import MainController
from utils.logger import get_logger
import qtawesome as qta

logger = get_logger(__name__)


class DashboardView(QWidget):
    """The landing dashboard view displaying key metrics, recent items, and analytics pane.

    Attributes:
        controller: Background orchestration controller.
        recent_layout: Layout handling the dynamic vertical list of recent items.
        table: Standard QTableWidget for holding low-stock alerts.
    """

    def __init__(self, controller: Optional[MainController] = None) -> None:
        """Initializes the DashboardView split-layout architecture."""
        super().__init__()
        self.controller = controller

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ------------------- LEFT PANE (Main Content) -------------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(24)

        header = QWidget()
        header.setObjectName("HeaderArea")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 24, 32, 8)

        title = QLabel("Dashboard")
        title.setObjectName("HeaderTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        left_layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setStyleSheet("background-color: transparent;")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(32, 0, 32, 32)
        content_layout.setSpacing(24)

        # Row 1: 4 Statistics Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(24)

        self.total_stats = StatsCard("Total Items", "0", "fa5s.boxes")
        self.loc_stats = StatsCard("Total Locations", "0", "fa5s.map")
        self.week_stats = StatsCard("Added This Week", "0", "fa5s.calendar-plus")
        self.tagged_stats = StatsCard("Tagged Items", "0", "fa5s.tags")

        stats_layout.addWidget(self.total_stats)
        stats_layout.addWidget(self.loc_stats)
        stats_layout.addWidget(self.week_stats)
        stats_layout.addWidget(self.tagged_stats)
        content_layout.addLayout(stats_layout)

        # Row 2: Recent Items Feed (Full Width in Left Pane)
        recent_widget = QWidget()
        self.recent_layout = QVBoxLayout(recent_widget)
        self.recent_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_layout.setSpacing(4)

        ri_title = QLabel("Recent Items")
        ri_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; margin-bottom: 12px; color: #f8fafc;"
        )
        self.recent_layout.addWidget(ri_title)

        content_layout.addWidget(recent_widget)
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        left_layout.addWidget(scroll_area)
        
        main_layout.addWidget(left_widget)

        # ------------------- RIGHT PANE (Floating Detail Panel) -------------------
        self.detail_panel = QWidget(self)
        self.detail_panel.setStyleSheet(
            "background-color: #0f1621; border-left: 1px solid #1e293b;"
        )
        detail_layout = QVBoxLayout(self.detail_panel)
        detail_layout.setContentsMargins(24, 24, 24, 24)

        dp_title = QLabel("Stock Alerts")
        dp_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #f8fafc; margin-bottom: 16px;"
        )

        img_placeholder = QLabel()
        img_placeholder.setPixmap(
            qta.icon("fa5s.chart-pie", color="#334155").pixmap(128, 128)
        )
        img_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_placeholder.setStyleSheet(
            "background-color: rgba(0,0,0,0.2); border-radius: 12px; margin-bottom: 24px;"
        )
        img_placeholder.setMinimumHeight(180)

        # Data Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Item", "Qty", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        detail_layout.addWidget(dp_title)
        detail_layout.addWidget(img_placeholder)
        detail_layout.addWidget(self.table)
        
        self.detail_panel.hide()

        # Floating Toggle Button
        self.toggle_btn = QToolButton(self)
        self.toggle_btn.setIcon(qta.icon("fa5s.chevron-left", color="#ffffff"))
        self.toggle_btn.setStyleSheet(
            "background-color: #3b82f6; border: none; border-radius: 4px; padding: 8px;"
        )
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self._toggle_detail_panel)
        self.panel_visible = False

        if self.controller:
            self.controller.data_updated.connect(self.refresh_data)

    def _toggle_detail_panel(self) -> None:
        """Toggles the visibility and layout of the floating detail overlay."""
        self.panel_visible = not self.panel_visible
        if self.panel_visible:
            self.detail_panel.show()
            self.detail_panel.raise_()
            self.toggle_btn.raise_()
            self.toggle_btn.setIcon(qta.icon("fa5s.chevron-right", color="#ffffff"))
        else:
            self.detail_panel.hide()
            self.toggle_btn.setIcon(qta.icon("fa5s.chevron-left", color="#ffffff"))
        
        self.resizeEvent(None)

    def resizeEvent(self, event) -> None:
        """Dynamically anchors the floating components to the right edge."""
        if getattr(super(), "resizeEvent", None) and event:
            super().resizeEvent(event)
            
        panel_width = 350
        # If visible, panel anchors to right edge; if hidden, it slides out (conceptually)
        panel_x = self.width() - panel_width if self.panel_visible else self.width()
        
        # We manually keep it anchored to height of the window natively
        self.detail_panel.setGeometry(panel_x, 0, panel_width, self.height())
        
        btn_width = 32
        btn_height = 32
        # Position button just left of the panel
        btn_x = panel_x - btn_width - 16
        if not self.panel_visible:
            # If panel is hidden, attach button near the right edge of screen
            btn_x = self.width() - btn_width - 16
            
        self.toggle_btn.setGeometry(btn_x, 24, btn_width, btn_height)

    def refresh_data(self) -> None:
        """Polls the assigned controller to repaint the dashboard UI metrics and tables."""
        if not self.controller:
            return

        logger.debug("DashboardView repainting UI based on new controller state.")

        num_items = len(self.controller.items)
        num_locs = len(self.controller.locations)
        tags_found = sum(1 for i in self.controller.items if i.tags)

        self.total_stats.findChild(QLabel, "StatsCardValue").setText(str(num_items))
        self.loc_stats.findChild(QLabel, "StatsCardValue").setText(str(num_locs))
        self.week_stats.findChild(QLabel, "StatsCardValue").setText(
            str(min(num_items, 5))
        )
        self.tagged_stats.findChild(QLabel, "StatsCardValue").setText(str(tags_found))

        # Clear existing recent items (we leave title at idx 0, wipe the rest)
        while self.recent_layout.count() > 1:
            item = self.recent_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        # Fill up to 5 items scrolling list
        count = 0
        for item_model in self.controller.items:
            if count >= 5:
                break
            # Fallback mock for location path
            path = "Unknown Location"
            if len(self.controller.locations) > 0:
                path = f"{self.controller.locations[0].name} > Floor"

            row = RecentItemRow(
                item_model.name, item_model.description, path, item_model.icon_name
            )
            self.recent_layout.addWidget(row)
            count += 1

        # Repopulate dynamic Data Table for Low Stock
        # Sort items: Low Supply (qty <= 3) first, then Enough Supply
        def get_status(qty: int) -> str:
            return "Low Supply" if qty <= 3 else "Enough Supply"
            
        sorted_items = sorted(
            self.controller.items, 
            key=lambda x: (0 if get_status(x.quantity) == "Low Supply" else 1, x.name)
        )
        
        self.table.setRowCount(len(sorted_items))
        
        for row_idx, item in enumerate(sorted_items):
            # Column 0: Item Name
            name_wi = QTableWidgetItem(item.name)
            self.table.setItem(row_idx, 0, name_wi)
            
            # Column 1: Quantity
            qty_wi = QTableWidgetItem(str(item.quantity))
            self.table.setItem(row_idx, 1, qty_wi)
            
            # Column 2: Status
            status_text = get_status(item.quantity)
            status_wi = QTableWidgetItem(status_text)
            
            self.table.setItem(row_idx, 2, status_wi)
