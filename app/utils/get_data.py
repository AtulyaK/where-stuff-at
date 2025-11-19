def populate_grid(self):
        from ui import ItemCard
        # Mock Data - In the future, this comes from your SQL Database
        mock_items = [
            {"id": 1, "name": "Arduino Uno R3", "cat": "Electronics", "qty": 5},
            {"id": 2, "name": "M3 Hex Bolts (100 pack)", "cat": "Hardware", "qty": 20},
            {"id": 3, "name": "PLA Filament (Red)", "cat": "3D Printing", "qty": 2},
            {"id": 4, "name": "Soldering Iron Station", "cat": "Tools", "qty": 1},
            {"id": 5, "name": "Raspberry Pi 4", "cat": "Electronics", "qty": 3},
            {"id": 6, "name": "USB-C Cables", "cat": "Cables", "qty": 12},
        ]

        # Grid Logic
        columns = 4 
        for i, data in enumerate(mock_items):
            row = i // columns
            col = i % columns
            
            # Create Card
            card = ItemCard(data['id'], data['name'], data['cat'], data['qty'])
            card.clicked.connect(handle_item_click(self)) # Connect signal
            
            self.grid_layout.addWidget(card, row, col)

def handle_item_click(self, item_id):
    print(f"Opening details for Item ID: {item_id}")