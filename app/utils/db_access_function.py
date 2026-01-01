import sqlite3
from typing import Optional, List, Dict, Any


# -------------------------------------------------
# Connection Helper
# -------------------------------------------------

def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Create a SQLite connection with foreign keys enabled.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# -------------------------------------------------
# 1. Get Items (Collated Across Locations)
# -------------------------------------------------

def get_items(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """
    Retrieve all item types, collating quantities across all locations.

    Returns one row per item type with total quantity summed from Inventory.
    """
    query = """
    SELECT
        IT.id AS item_type_id,
        IT.name,
        IT.description,
        IT.image_path,
        SUM(I.quantity) AS total_quantity
    FROM ItemTypes IT
    LEFT JOIN Inventory I ON IT.id = I.item_type_id
    GROUP BY IT.id, IT.name, IT.description, IT.image_path
    ORDER BY IT.name;
    """
    cur = conn.execute(query)
    return [dict(row) for row in cur.fetchall()]


# -------------------------------------------------
# 2. Add Item
# -------------------------------------------------

def add_item(
    conn: sqlite3.Connection,
    name: str,
    description: Optional[str] = None,
    category_id: Optional[int] = None,
    image_path: Optional[str] = None
) -> int:
    """
    Add a new item to the ItemTypes catalog.

    Returns the new item_type_id.
    """
    query = """
    INSERT INTO ItemTypes (name, description, category_id, image_path)
    VALUES (?, ?, ?, ?);
    """
    cur = conn.execute(query, (name, description, category_id, image_path))
    conn.commit()
    return cur.lastrowid


# -------------------------------------------------
# 3. Update Item
# -------------------------------------------------

def update_item(
    conn: sqlite3.Connection,
    item_type_id: int,
    name: str,
    description: Optional[str],
    category_id: Optional[int],
    image_path: Optional[str]
) -> None:
    """
    Update an existing item in the catalog.
    """
    query = """
    UPDATE ItemTypes
    SET name = ?, description = ?, category_id = ?, image_path = ?
    WHERE id = ?;
    """
    conn.execute(query, (name, description, category_id, image_path, item_type_id))
    conn.commit()


# -------------------------------------------------
# 4. Remove Item
# -------------------------------------------------

def delete_item(conn: sqlite3.Connection, item_type_id: int) -> None:
    """
    Delete an item type.

    Cascades to Inventory and PackingList_Items.
    """
    conn.execute("DELETE FROM ItemTypes WHERE id = ?;", (item_type_id,))
    conn.commit()


# -------------------------------------------------
# 5. Inventory
# -------------------------------------------------

def get_inventory_by_location(
    conn: sqlite3.Connection,
    location_id: int
) -> List[Dict[str, Any]]:
    """
    Retrieve all inventory items stored at a specific location.
    """
    query = """
    SELECT
        I.id AS inventory_id,
        IT.id AS item_type_id,
        IT.name,
        I.quantity,
        I.min_stock_level,
        I.expiry_date
    FROM Inventory I
    JOIN ItemTypes IT ON I.item_type_id = IT.id
    WHERE I.location_id = ?;
    """
    cur = conn.execute(query, (location_id,))
    return [dict(row) for row in cur.fetchall()]


def add_inventory(
    conn: sqlite3.Connection,
    item_type_id: int,
    location_id: int,
    quantity: int,
    min_stock_level: Optional[int] = None,
    expiry_date: Optional[str] = None
) -> int:
    """
    Add an inventory entry linking an item to a location.
    """
    query = """
    INSERT INTO Inventory (item_type_id, location_id, quantity, min_stock_level, expiry_date)
    VALUES (?, ?, ?, ?, ?);
    """
    cur = conn.execute(
        query,
        (item_type_id, location_id, quantity, min_stock_level, expiry_date)
    )
    conn.commit()
    return cur.lastrowid


def update_inventory(
    conn: sqlite3.Connection,
    inventory_id: int,
    quantity: int,
    min_stock_level: Optional[int],
    expiry_date: Optional[str]
) -> None:
    """
    Update inventory quantity or metadata.
    """
    query = """
    UPDATE Inventory
    SET quantity = ?, min_stock_level = ?, expiry_date = ?
    WHERE id = ?;
    """
    conn.execute(query, (quantity, min_stock_level, expiry_date, inventory_id))
    conn.commit()


def delete_inventory(conn: sqlite3.Connection, inventory_id: int) -> None:
    """
    Remove an inventory entry.
    """
    conn.execute("DELETE FROM Inventory WHERE id = ?;", (inventory_id,))
    conn.commit()


# -------------------------------------------------
# 6. Create Packing List
# -------------------------------------------------

def create_packing_list(conn: sqlite3.Connection, name: str) -> int:
    """
    Create a new packing list.

    Returns the packing_list_id.
    """
    cur = conn.execute(
        "INSERT INTO PackingLists (name) VALUES (?);",
        (name,)
    )
    conn.commit()
    return cur.lastrowid


def add_item_to_packing_list(
    conn: sqlite3.Connection,
    packing_list_id: int,
    item_type_id: int,
    quantity_needed: int
) -> int:
    """
    Add an item to a packing list.
    """
    query = """
    INSERT INTO PackingList_Items (packing_list_id, item_type_id, quantity_needed)
    VALUES (?, ?, ?);
    """
    cur = conn.execute(query, (packing_list_id, item_type_id, quantity_needed))
    conn.commit()
    return cur.lastrowid


# -------------------------------------------------
# 7. Update Packing List
# -------------------------------------------------

def update_packing_list_name(
    conn: sqlite3.Connection,
    packing_list_id: int,
    name: str
) -> None:
    """
    Rename a packing list.
    """
    conn.execute(
        "UPDATE PackingLists SET name = ? WHERE id = ?;",
        (name, packing_list_id)
    )
    conn.commit()


def update_packing_list_item(
    conn: sqlite3.Connection,
    packing_list_item_id: int,
    quantity_needed: int,
    packed: bool
) -> None:
    """
    Update quantity or packed status for an item in a packing list.
    """
    conn.execute(
        """
        UPDATE PackingList_Items
        SET quantity_needed = ?, packed = ?
        WHERE id = ?;
        """,
        (quantity_needed, int(packed), packing_list_item_id)
    )
    conn.commit()


# -------------------------------------------------
# 8. Create Location
# -------------------------------------------------

def create_location(
    conn: sqlite3.Connection,
    name: str,
    parent_id: Optional[int] = None
) -> int:
    """
    Create a new storage location.
    """
    cur = conn.execute(
        "INSERT INTO locations (name, parent_id) VALUES (?, ?);",
        (name, parent_id)
    )
    conn.commit()
    return cur.lastrowid


# -------------------------------------------------
# 9. Update Location Details
# -------------------------------------------------

def update_location(
    conn: sqlite3.Connection,
    location_id: int,
    name: str,
    parent_id: Optional[int]
) -> None:
    """
    Update a location's name or parent.
    """
    conn.execute(
        """
        UPDATE locations
        SET name = ?, parent_id = ?
        WHERE id = ?;
        """,
        (name, parent_id, location_id)
    )
    conn.commit()


# -------------------------------------------------
# 10. Delete / Archive Location
# -------------------------------------------------

def delete_location(conn: sqlite3.Connection, location_id: int) -> None:
    """
    Permanently delete a location.

    Cascades to Inventory.
    """
    conn.execute("DELETE FROM locations WHERE id = ?;", (location_id,))
    conn.commit()


# -------------------------------------------------
# 11. CRUD Categories
# -------------------------------------------------

def create_category(
    conn: sqlite3.Connection,
    name: str,
    parent_id: Optional[int] = None
) -> int:
    """
    Create a new item category.
    """
    cur = conn.execute(
        "INSERT INTO categories (name, parent_id) VALUES (?, ?);",
        (name, parent_id)
    )
    conn.commit()
    return cur.lastrowid


def get_categories(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """
    Retrieve all categories.
    """
    cur = conn.execute(
        "SELECT id, name, parent_id FROM categories ORDER BY name;"
    )
    return [dict(row) for row in cur.fetchall()]


def update_category(
    conn: sqlite3.Connection,
    category_id: int,
    name: str,
    parent_id: Optional[int]
) -> None:
    """
    Update a category.
    """
    conn.execute(
        """
        UPDATE categories
        SET name = ?, parent_id = ?
        WHERE id = ?;
        """,
        (name, parent_id, category_id)
    )
    conn.commit()


def delete_category(conn: sqlite3.Connection, category_id: int) -> None:
    """
    Delete a category.

    Items referencing it will have category_id set to NULL.
    """
    conn.execute("DELETE FROM categories WHERE id = ?;", (category_id,))
    conn.commit()
