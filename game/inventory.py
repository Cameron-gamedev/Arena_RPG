
from game.items.item import Item

class Inventory:
    def __init__(self, size=20):
        self.size = size
        self.slots = [None] * size

    # -------------------------
    # Check if inventory is full
    # -------------------------
    def is_full(self):
        return all(slot is not None for slot in self.slots)

    # -------------------------
    # Find an existing stack for a consumable
    # -------------------------
    def find_stack(self, item):
        if not item.stackable:
            return None

        for slot in self.slots:
            if slot is None:
                continue

            # Must match item_type AND effect
            if (slot.item_type == item.item_type and
                slot.effect == item.effect and
                slot.stackable):
                return slot

        return None

    # -------------------------
    # Add an item to inventory
    # -------------------------
    def add_item(self, item):
        # 1. Try stacking if possible
        if item.stackable:
            existing_stack = self.find_stack(item)

            if existing_stack:
                # Add as much as possible
                space_left = existing_stack.max_stack - existing_stack.quantity

                if space_left > 0:
                    amount_to_add = min(space_left, item.quantity)
                    existing_stack.quantity += amount_to_add
                    item.quantity -= amount_to_add

                # If item still has quantity left, overflow into new slot
                if item.quantity > 0:
                    # Try to place overflow in empty slot
                    for i in range(self.size):
                        if self.slots[i] is None:
                            # Create a new stack with remaining quantity
                            self.slots[i] = Item(
                                name=item.name,
                                item_type=item.item_type,
                                effect=item.effect,
                                stackable=True,
                                quantity=item.quantity
                            )
                            return True

                    # No empty slot for overflow
                    return False

                return True

        # 2. If not stackable or no stack found, place in empty slot
        for i in range(self.size):
            if self.slots[i] is None:
                self.slots[i] = item
                return True

        # 3. No empty slot
        return False

    # -------------------------
    # Remove an item from a slot
    # -------------------------
    def remove_item(self, index):
        if index < 0 or index >= self.size:
            return None

        item = self.slots[index]
        self.slots[index] = None
        return item
