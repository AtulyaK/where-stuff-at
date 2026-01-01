"""
1. get items (collate the items based on name across locations)
2. add item
3. update item
4. remove item
5. inventory
6. create packing list
7. update packing list
8. create location
9. update location details
10. delete/archive location
11. CRUD categories
"""

# 1. get items (collate the items based on name across locations)
def get_items():
    query = """
        SELECT it.name, in.quantity, in.min_stock_level, loc.id, cat.id FROM Inventory as in
        INNER JOIN ItemTypes as it ON in.item_type_id = it.id
        INNER JOIN Location as loc ON in.location_id = loc.id
        JOIN Categories as cat ON it.category_id = cat.id
        GROUP BY ;
    """
    return

# 5. inventory
def get_inventory(location_id):
    query = """
        SELECT it.name, in.quantity, in.min_stock_level, loc.id FROM Inventory as in
        INNER JOIN ItemTypes as it ON in.item_type_id = it.id
        INNER JOIN Location as loc ON in.location_id = loc.id
        WHERE in.location_id = location_id;
    """
    return

