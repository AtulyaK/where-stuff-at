from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QScrollArea, QGridLayout, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from utils import populate_grid
class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Storage Application")
        self.resize(1200, 800)

        # Main Container
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        # --- Left Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setObjectName("Sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 20, 0, 20)
        
        # Nav Buttons
        nav_items = ["Dashboard", "Items", "Locations", "Packing Lists", "Settings"]
        for nav in nav_items:
            btn = QPushButton(nav)
            btn.setCheckable(True)
            if nav == "Items": btn.setChecked(True) # Set active tab
            self.sidebar_layout.addWidget(btn)
        
        self.sidebar_layout.addStretch() 

        # --- Right Content Area ---
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        
        # Top Control Bar
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(60)
        self.top_bar.setStyleSheet("border-bottom: 1px solid #ddd; background: white;")
        # (You can add search bars/filters here later)
        
        # Grid Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: #f4f7f6;")
        
        self.grid_container = QWidget()
        self.grid_container.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        
        self.scroll.setWidget(self.grid_container)
        
        # Assemble Right Side
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.scroll)

        # Assemble Main Layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

        # Load Initial Data
        populate_grid(self)