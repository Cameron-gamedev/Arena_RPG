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
        self.slots = {slot:None for slot in slot_rules}
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
        return(
            name.isidentifier()
            and name[0].islower()
            and not name.endswith("_")
        )
    
    def _validate_slot(self, slot):
        # slot must exist
        if slot not in self.slot_rules:
            raise ValueError(f" - Slot '{slot}' does not exist in this equipment layout.")
    # ------------------------------------
    # Item Validation
    # ------------------------------------
    def _validate_item(self, item):
        # Item must have a valid item_type
        if not hasattr(item, "item_type"):
            raise ValueError(
                f" - Item{item} has no 'item_type' attribute.\n"
                " - All equippable items must define 'item_type' "
            )
        item_type = item.item_type

        # Item must be a string
        if not isinstance(item_type, str):
            raise ValueError(
                f" - Invalid item_type for item '{item}'.\n"
                " - 'item_type must be a string."
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
    # Item Modifiers
    # ------------------------------------       
    
    def _validate_modifier_value(self, mods, item):
        # Validate each modifier entry
        for stat, entry in mods.items():
            if not isinstance(entry, dict):
                raise ValueError(
                    f"Modifier for stat '{stat}' on item '{item}' must be a dictionary.\n"
                    "Expected: {'value': number, 'is_percent': bool}"
                )

            if "value" not in entry:
                raise ValueError(
                    f"Modifier for stat '{stat}' on item '{item}' is missing 'value'."
                )

            if "is_percent" not in entry:
                raise ValueError(
                    f"Modifier for stat '{stat}' on item '{item}' is missing 'is_percent'."
                )

            value = entry["value"]
            is_percent = entry["is_percent"]

            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"Modifier value for stat '{stat}' on item '{item}' must be a number.\n"
                    f"Got: {value} ({type(value).__name__})"
                )

            if not isinstance(is_percent, bool):
                raise ValueError(
                    f"'is_percent' for stat '{stat}' on item '{item}' must be a boolean.\n"
                    f"Got: {is_percent} ({type(is_percent).__name__})"
                )
            
    def _accumulate_modifier(self, totals, stat, entry):
        """
        Add a single modifier entry into the totals dictionary.
        totals = {
            'flat': {stat: value},
            'percent': {stat: value}
        }
        """
        value = entry["value"]
        is_percent = entry["is_percent"]

        if is_percent:
            totals["percent"][stat] = totals["percent"].get(stat, 0) + value
        else:
            totals["flat"][stat] = totals["flat"].get(stat, 0) + value
    
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
        # Add flat first
        total = base + flat

        # Apply additive percent
        total *= (1 + percent)

        return total

    def _validate_modifiers(self, item):
        """
        Validates the modifiers dictionary.
        Empty modifiers {} are allowed.
        """
        if not hasattr(item, "modifiers"):
            raise ValueError(
                f"Item '{item}' is missing a 'modifiers' attribute.\n"
                "Items must define a modifiers dictionary (empty dict allowed)."
            )

        mods = item.modifiers

        # Allow empty modifiers
        if mods is None or mods == {}:
            return

        if not isinstance(mods, dict):
            raise ValueError(
                f"Item '{item}' has invalid modifiers type {type(mods).__name__}.\n"
                "Modifiers must be a dictionary."
            )

        # Validate each modifier entry
        self._validate_modifier_value(mods, item)


    def get_total_modifiers(self, base_stats=None):
        """
        Returns final stat values after applying flat and percent modifiers.
        base_stats: optional dict of base stat values.
        If base_stats is None, treat base as 0.
        """
        totals = {
            "flat": {},
            "percent": {}
        }

        # Step 1: accumulate modifiers
        for slot, item in self.slots.items():
            if item is None:
                continue

            self._validate_modifiers(item)

            for stat, entry in item.modifiers.items():
                self._accumulate_modifier(totals, stat, entry)

        

        return totals

    # ------------------------------------
    # Item Management
    # ------------------------------------
    def can_equip(self, slot, item):
        
        # Item & Slot validation
        self._validate_slot(slot)
        self._validate_item(item)

        # Item type must be allowed in this slot
        allowed_types = self.slot_rules[slot]
        return item.item_type in allowed_types
    
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
        # Validate slots exists
        self._validate_slot(slot)

        if self.slots[slot] is None:
            return False # If slot is empty, return false
        
        # Remove and return item
        old_item = self.slots[slot]
        self.slots[slot] = None
        return old_item
    
    