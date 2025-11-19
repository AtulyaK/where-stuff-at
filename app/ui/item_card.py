from PyQt6.QtWidgets import QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
class ItemCard(QFrame):
    # Signal: Emits the Item ID when the card is clicked
    clicked = pyqtSignal(int)

    def __init__(self, item_id, name, category, qty):
        super().__init__()
        self.item_id = item_id
        
        # Setup UI properties
        self.setFixedSize(200, 260)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("ItemCard") # ID for QSS styling
        
        # Internal Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # A. Thumbnail Placeholder
        self.lbl_image = QLabel("No Image")
        self.lbl_image.setFixedSize(178, 120)
        self.lbl_image.setStyleSheet("background-color: #eee; border-radius: 8px; color: #888;")
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        # B. Text Data
        self.lbl_name = QLabel(name)
        self.lbl_name.setObjectName("CardTitle")
        self.lbl_name.setWordWrap(True)
        
        self.lbl_cat = QLabel(category)
        self.lbl_cat.setObjectName("CardSub")
        
        self.lbl_qty = QLabel(f"Total Qty: {qty}")
        self.lbl_qty.setObjectName("CardAccent")
        
        # Add widgets to layout
        layout.addWidget(self.lbl_image)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.lbl_cat)
        layout.addWidget(self.lbl_qty)
        layout.addStretch() 
        
        self.setLayout(layout)

    def mousePressEvent(self, event):
        # Trigger the custom signal when clicked
        self.clicked.emit(self.item_id)
        super().mousePressEvent(event)