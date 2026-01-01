# Storage App – Database README

This README documents the SQLite database structure used by the **Storage App**. It explains the purpose of each table, how tables relate to one another, and important implementation details for developers working with or extending the database.

---

## Overview

The database is designed around a few core concepts:

* **Locations**: Physical storage areas arranged in a hierarchy
* **Categories**: Hierarchical classification system for items
* **ItemTypes**: A centralized catalog describing what items are
* **Inventory**: Tracks quantities of items at specific locations
* **Packing Lists**: User-defined lists for trips or projects
* **Packing List Items**: The items required for each packing list

SQLite is used as the database engine, with foreign key constraints enabled to maintain data integrity.

---

## Tables

### `locations`

Stores physical storage locations in a hierarchical structure (for example: `House → Garage → Shelf`).

```sql
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES locations (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

**Columns**

* `id`: Unique identifier for the location
* `name`: Display name of the location
* `parent_id`: References another location to create a hierarchy

**Behavior**

* Deleting a parent location sets child locations to top-level
* Supports unlimited nesting depth

---

### `categories`

Defines hierarchical categories used to classify items (for example: `Electronics → Cables`).

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES categories (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

**Columns**

* `id`: Unique identifier for the category
* `name`: Category name
* `parent_id`: Parent category (nullable)

---

### `ItemTypes`

Represents the master catalog of items. This table defines *what* an item is, independent of where it is stored.

```sql
CREATE TABLE ItemTypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    category_id INTEGER,
    image_path TEXT,
    FOREIGN KEY (category_id) REFERENCES categories (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

**Columns**

* `id`: Unique identifier
* `name`: Item name (e.g., "AA Batteries")
* `description`: Optional descriptive text
* `category_id`: References `categories.id`
* `image_path`: Path or URL to an image representing the item

**Notes**

* Items are not deleted if their category is removed

---

### `Inventory`

Tracks the actual stock levels of items at specific locations. This table represents the intersection of items and locations.

```sql
CREATE TABLE Inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_type_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    min_stock_level INTEGER,
    expiry_date TEXT,
    FOREIGN KEY (item_type_id) REFERENCES ItemTypes (id)
        ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations (id)
        ON DELETE CASCADE
);
```

**Columns**

* `id`: Unique identifier
* `item_type_id`: References `ItemTypes.id`
* `location_id`: References `locations.id`
* `quantity`: Number of items on hand
* `min_stock_level`: Optional restocking threshold
* `expiry_date`: Optional expiration date (`YYYY-MM-DD`)

**Notes**

* Deleting an item or location removes associated inventory records
* Enables per-location stock tracking

---

### `PackingLists`

Stores user-created packing lists for trips or projects.

```sql
CREATE TABLE PackingLists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    creation_date TEXT NOT NULL DEFAULT (DATETIME('now'))
);
```

**Columns**

* `id`: Unique identifier
* `name`: Name of the packing list (e.g., "Camping Trip")
* `creation_date`: Automatically generated creation timestamp

---

### `PackingList_Items`

Defines which items are required for each packing list and tracks packing progress.

```sql
CREATE TABLE PackingList_Items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    packing_list_id INTEGER NOT NULL,
    item_type_id INTEGER NOT NULL,
    quantity_needed INTEGER NOT NULL DEFAULT 1,
    packed INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (packing_list_id) REFERENCES PackingLists (id)
        ON DELETE CASCADE,
    FOREIGN KEY (item_type_id) REFERENCES ItemTypes (id)
        ON DELETE CASCADE
);
```

**Columns**

* `id`: Unique identifier
* `packing_list_id`: References `PackingLists.id`
* `item_type_id`: References `ItemTypes.id`
* `quantity_needed`: Quantity required for the list
* `packed`: Boolean flag (`0 = false`, `1 = true`)

---

## Relationships Summary

* Locations form a self-referencing hierarchy
* Categories form a self-referencing hierarchy
* ItemTypes belong to categories
* Inventory links ItemTypes to Locations
* PackingLists contain many PackingList_Items
* ItemTypes can appear in multiple packing lists

---

## SQLite Implementation Notes

* **Foreign Keys** must be enabled explicitly:

  ```sql
  PRAGMA foreign_keys = ON;
  ```

* **Booleans** are stored as integers (`0` or `1`)

* **Dates and times** are stored as ISO 8601 strings
