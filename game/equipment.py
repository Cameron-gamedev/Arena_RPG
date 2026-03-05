from game.items.item_types import ItemType
import warnings


class Equipment:
    def __init__(self, slot_rules):
        # Validate slot names
        for slot in slot_rules:
            if not self._is_valid_slot_name(slot):
                raise ValueError(
                    f" - Invalid slot name: {slot}.\n"
                    " - Slot names must use '_' and start with a lowercase letter."
                    " - Contain only letters, numbers, and underscores. Must not end with '_'"
                )

        # Defensive copy of slot rules
        self.slot_rules = {
            slot: {
                **allowed,
                "allowed_types": allowed["allowed_types"][:]
            }
            for slot, allowed in slot_rules.items()
        }

        # Initialize empty slots
        self.slots = {slot: None for slot in slot_rules}

    # ------------------------------------
    # Item conversion
    # ------------------------------------
    def _convert_item_type(self, item, slot_name):
        try:
            return ItemType(item.item_type)
        except ValueError as e:
            raise ValueError(
                f"Error while equipping item '{item}' "
                f"(type='{item.item_type}') into slot '{slot_name}': {e}"
            ) from e

    # ------------------------------------
    # Slot Validation
    # ------------------------------------
    def _is_valid_slot_name(self, name):
        # snake_case + numbers, must start with a letter
        return (
            name.isidentifier()
            and name[0].islower()
            and not name.endswith("_")
        )

    def _validate_slot(self, slot):
        if slot not in self.slot_rules:
            raise ValueError(f" - Slot '{slot}' does not exist in this equipment layout.")

    # ------------------------------------
    # Item Validation
    # ------------------------------------
    def _validate_item(self, item):
        if not hasattr(item, "item_type"):
            raise ValueError(
                f" - Item {item} has no 'item_type' attribute.\n"
                " - All equippable items must define 'item_type'."
            )

        item_type = item.item_type
        if not isinstance(item_type, str):
            raise ValueError(
                f" - Invalid item_type for item '{item}'.\n"
                " - 'item_type' must be a string."
            )

    def _validate_item_type(self, slot_name, item_type, item):
        slot_def = self.slot_rules[slot_name]
        allowed_raw = slot_def.get("allowed_types", [])

        normalized_allowed = []
        for raw in allowed_raw:
            clean = raw.strip().lower()
            if clean != raw:
                warnings.warn(
                    f"Normalized slot allowed type '{raw}' → '{clean}'",
                    UserWarning
                )
            normalized_allowed.append(clean)

        if item_type.value not in normalized_allowed:
            raise ValueError(
                f"Cannot equip item '{item}' (type='{item_type.value}') "
                f"into slot '{slot_name}'. Allowed types: {normalized_allowed}"
            )

    # ------------------------------------
    # Item Modifiers (NEW FORMAT)
    # ------------------------------------
    def _validate_modifiers(self, item):
        """
        Validates the modifiers dictionary for the NEW format:
            modifiers = {
                "flat":    {stat: number, ...},
                "percent": {stat: number, ...}
            }
        """
        if not hasattr(item, "modifiers"):
            raise ValueError(
                f"Item '{item}' is missing a 'modifiers' attribute.\n"
                "Items must define a modifiers dictionary (empty dict allowed)."
            )

        mods = item.modifiers

        # Allow empty or None
        if mods is None or mods == {}:
            return

        if not isinstance(mods, dict):
            raise ValueError(
                f"Item '{item}' has invalid modifiers type {type(mods).__name__}.\n"
                "Modifiers must be a dictionary."
            )

        flat = mods.get("flat", {})
        percent = mods.get("percent", {})

        if not isinstance(flat, dict) or not isinstance(percent, dict):
            raise ValueError(
                f"Item '{item}' modifiers must contain 'flat' and 'percent' dicts.\n"
                f"Got: flat={type(flat).__name__}, percent={type(percent).__name__}"
            )

        # Validate flat values
        for stat, value in flat.items():
            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"Flat modifier for stat '{stat}' on item '{item}' must be a number.\n"
                    f"Got: {value} ({type(value).__name__})"
                )

        # Validate percent values
        for stat, value in percent.items():
            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"Percent modifier for stat '{stat}' on item '{item}' must be a number.\n"
                    f"Got: {value} ({type(value).__name__})"
                )

    def _apply_percent_math(self, base, flat, percent):
        """
        Apply flat and percent modifiers to a base stat.
        Percent modifiers stack additively.
        Example:
            base = 10
            flat = 3
            percent = 0.30  # 30%
            result = (10 + 3) * (1 + 0.30) = 16.9
        """
        total = base + flat
        total *= (1 + percent)
        return total

    def get_total_modifiers(self, base_stats=None):
        """
        Aggregates all equipment modifiers into:
            {
                "flat":    {stat: total_flat_bonus},
                "percent": {stat: total_percent_bonus}
            }
        base_stats is unused here but kept for compatibility.
        """
        totals = {
            "flat": {},
            "percent": {}
        }

        for slot, item in self.slots.items():
            if item is None:
                continue

            self._validate_modifiers(item)
            mods = item.modifiers or {"flat": {}, "percent": {}}

            # Flat modifiers
            for stat, value in mods.get("flat", {}).items():
                totals["flat"][stat] = totals["flat"].get(stat, 0) + value

            # Percent modifiers
            for stat, value in mods.get("percent", {}).items():
                totals["percent"][stat] = totals["percent"].get(stat, 0) + value

        return totals

    # ------------------------------------
    # Item Management
    # ------------------------------------
    def can_equip(self, slot, item):
        self._validate_slot(slot)
        self._validate_item(item)

        # Convert item type
        try:
            item_type = self._convert_item_type(item, slot)
        except ValueError:
            return False

        # Validate compatibility
        try:
            self._validate_item_type(slot, item_type, item)
        except ValueError:
            return False

        return True

    def equip_item(self, slot, item):
        self._validate_slot(slot)
        self._validate_item(item)

        # Convert + validate
        item_type = self._convert_item_type(item, slot)
        self._validate_item_type(slot, item_type, item)

        old_item = self.slots[slot]
        self.slots[slot] = item
        return old_item

    def unequip_item(self, slot):
        self._validate_slot(slot)

        if self.slots[slot] is None:
            return False

        old_item = self.slots[slot]
        self.slots[slot] = None
        return old_item
