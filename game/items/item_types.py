from enum import StrEnum
import warnings

# Track which incorrect values we've already warned about
_seen_itemtype_normalizations = set()


class ItemType(StrEnum):
    WEAPON = "weapon"
    SHIELD = "shield"
    ARMOR = "armor"
    RING = "ring"
    AMULET = "amulet"
    FOCUS = "focus"
    TWO_HANDED_WEAPON = "two_handed_weapon"

    @classmethod
    def _missing_(cls, value):
        # Only attempt normalization for strings
        if isinstance(value, str):
            original = value
            normalized = value.strip().lower()

            # If normalization changed the value, warn once
            if normalized != original and original not in _seen_itemtype_normalizations:
                warnings.warn(
                    f"Normalized '{original}' → '{normalized}'",
                    UserWarning
                )
                _seen_itemtype_normalizations.add(original)

            # Try to match the normalized value
            for member in cls:
                if member.value == normalized:
                    return member

        # If we reach here, it's invalid
        allowed = [member.value for member in cls]
        raise ValueError(
            f"Invalid ItemType: '{value}'. Allowed types: {allowed}"
        )