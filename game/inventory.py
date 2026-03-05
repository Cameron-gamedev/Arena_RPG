
from game.items.item import Item

class Inventory:
    def __init__(self, size=20):
        self.size = size
        self.slots = [None] * size

    # ============================================================
    # BASIC CHECKS
    # ============================================================
    def is_full(self):
        return all(slot is not None for slot in self.slots)

    # ============================================================
    # ITEM TYPE FILTERS
    # ============================================================
    def get_consumables(self):
        """Return list of (slot_index, item) for consumables."""
        consumables = []
        for i, item in enumerate(self.slots):
            if item and item.item_type == "consumable":
                consumables.append((i, item))
        return consumables


    def get_equipment(self):
        """Return list of (slot_index, item) for items that can be equipped."""
        from game.slots.slot_definitions import SLOT_RULES

        # Build a set of all allowed equipment types
        allowed_types = set()
        for slot, rule in SLOT_RULES.items():
            for t in rule["allowed_types"]:
                allowed_types.add(t)

        equipment = []
        for i, item in enumerate(self.slots):
            if item is None:
                continue
            if item.item_type in allowed_types:
                equipment.append((i, item))

        return equipment

    # ============================================================
    # STACKING LOGIC
    # ============================================================
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

    # ============================================================
    # ADD ITEM
    # ============================================================
    def add_item(self, item):
        # 1. Try stacking
        if item.stackable:
            existing_stack = self.find_stack(item)

            if existing_stack:
                space_left = existing_stack.max_stacks - existing_stack.quantity

                if space_left > 0:
                    amount_to_add = min(space_left, item.quantity)
                    existing_stack.quantity += amount_to_add
                    item.quantity -= amount_to_add

                # Overflow into new slot
                if item.quantity > 0:
                    for i in range(self.size):
                        if self.slots[i] is None:
                            self.slots[i] = Item(
                                name=item.name,
                                item_type=item.item_type,
                                effect=item.effect,
                                stackable=True,
                                quantity=item.quantity
                            )
                            return True
                    return False

                return True

        # 2. Not stackable or no stack found → place in empty slot
        for i in range(self.size):
            if self.slots[i] is None:
                self.slots[i] = item
                return True

        # 3. No empty slot
        return False

    # ============================================================
    # REMOVE ITEM
    # ============================================================
    def remove_item(self, index):
        if index < 0 or index >= self.size:
            return None

        item = self.slots[index]
        self.slots[index] = None
        return item
    

    def get_all_items(self):
        # Return list of (slot_index, item) for all non-empty inventory slots.
        return [(i, item) for i, item in enumerate(self.slots) if item is not None]