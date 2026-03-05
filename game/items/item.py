from game.items.item_types import ItemType


class Item:
    def __init__(
        self,
        name,
        item_type,
        effect=None,
        stackable=False,
        quantity=1,
        attack_bonus=0,
        defense_bonus=0,
        crit_bonus=0,
        modifiers=None
    ):
        self.name = name

        # Normalize item_type using ItemType enum
        try:
            self.item_type = ItemType(item_type).value
        except Exception:
            self.item_type = item_type  # fallback if needed

        # -----------------------------
        # ITEM EFFECT (for consumables)
        # -----------------------------
        # Examples:
        #   - restore_instant
        #   - restore_over_time
        #   - status (BuffStrength, Poison, etc.)
        self.effect = effect or None

        # -----------------------------
        # STACKING & QUANTITY
        # -----------------------------
        self.stackable = stackable
        self.quantity = quantity
        self.max_stacks = 10

        # -----------------------------
        # EQUIPMENT BONUSES
        # -----------------------------
        # These are read directly by Equipment.get_total_modifiers()
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.crit_bonus = crit_bonus

        # -----------------------------
        # MODIFIERS (NEW FORMAT)
        # -----------------------------
        # Must always be:
        #   modifiers = {
        #       "flat": {"strength": 2, ...},
        #       "percent": {"attack": 0.10, ...}
        #   }
        # If missing, normalize it.
        if modifiers is None:
            self.modifiers = {"flat": {}, "percent": {}}
        else:
            # Normalize missing keys
            self.modifiers = {
                "flat": modifiers.get("flat", {}),
                "percent": modifiers.get("percent", {})
            }

    # ============================================================
    # ITEM UTILITY
    # ============================================================
    def is_consumable(self):
        return self.item_type == "consumable"

    def can_stack_with(self, other):
        return (
            self.stackable
            and other.stackable
            and self.name == other.name
            and self.quantity < self.max_stacks
        )

    def add_stack(self, amount=1):
        if not self.stackable:
            return False
        self.quantity = min(self.max_stacks, self.quantity + amount)
        return True

    def remove_stack(self, amount=1):
        if not self.stackable:
            return False
        self.quantity -= amount
        if self.quantity <= 0:
            return True  # signal to remove item from inventory
        return False

    def __repr__(self):
        return f"<Item {self.name} x{self.quantity}>"
