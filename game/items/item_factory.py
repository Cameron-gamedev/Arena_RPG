from game.items.item import Item
from game.items.item_definitions import ITEM_DEFINITIONS

def create_item(item_id):
    """
    Creates a new Item object from the ITEM_DEFINITIONS dictionary.
    item_id: string key in ITEM_DEFINITIONS
    """
    if item_id not in ITEM_DEFINITIONS:
        raise ValueError(f"Unknown item_id '{item_id}' in ITEM_DEFINITIONS")

    data = ITEM_DEFINITIONS[item_id]

    # Unpack dictionary directly into Item constructor
    return Item(**data)
