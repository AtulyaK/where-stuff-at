"""Data models for the Where's My Stuff application.

Defines the structure of core business objects such as Items and Locations.
Adheres strictly to PEP 8 and the Google Python Style Guide.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Location:
    """Represents a physical location where items are stored.

    Attributes:
        id: A unique identifier for the location.
        name: The display name of the location.
        loc_type: The type of location (e.g., 'room', 'region', 'specific').
        parent_id: The ID of the parent location, if any (e.g. region belongs to room).
    """

    id: str
    name: str
    loc_type: str
    parent_id: Optional[str] = None


@dataclass
class Item:
    """Represents an inventory item.

    Attributes:
        id: A unique identifier for the item.
        name: The name of the item.
        description: A text description of the item.
        tags: A list of string tags associated with the item.
        date_added: The timestamp when the item was created.
        icon_name: The icon identifier used for UI representation.
        location_id: The ID of the location where the item is stored.
    """

    id: str
    name: str
    description: str
    quantity: int = 1
    tags: List[str] = field(default_factory=list)
    date_added: datetime = field(default_factory=datetime.now)
    icon_name: str = "fa5s.box"
    location_id: Optional[str] = None
