import json
from pathlib import Path
from copy import deepcopy

from game.player import Player
from game.items.item_definitions import ITEM_DEFINITIONS
from game.items.item_factory import create_item

SAVE_VERSION = 1
DEFAULT_SAVE_PATH = Path("saves/checkpoint_slot_1.json")


_NAME_TO_ITEM_ID = {data["name"]: item_id for item_id, data in ITEM_DEFINITIONS.items()}


def _effect_to_serializable(effect):
    safe = []
    for entry in effect:
        data = {}
        for key, value in entry.get("data", {}).items():
            if key == "applier":
                continue
            if isinstance(value, (str, int, float, bool, list, dict)) or value is None:
                data[key] = deepcopy(value)

        safe.append(
            {
                "name": entry.get("name"),
                "type": entry.get("type"),
                "duration": entry.get("duration", 0),
                "data": data,
            }
        )
    return safe


def _serialize_item(item):
    item_id = _NAME_TO_ITEM_ID.get(item.name)
    if item_id is None:
        raise ValueError(f"Cannot serialize unknown item '{item.name}'.")
    return {"item_id": item_id, "quantity": item.quantity}


def serialize_player(player):
    inv = []
    for item in player.inventory.slots:
        inv.append(_serialize_item(item) if item else None)

    equipment = {}
    for slot, item in player.equipment.slots.items():
        equipment[slot] = _serialize_item(item) if item else None

    return {
        "name": player.name,
        "class_name": player.player_class_name,
        "level": player.level,
        "current_xp": player.current_xp,
        "base_stats": deepcopy(player.base_stats),
        "base_atk": player.base_atk,
        "base_def": player.base_def,
        "resources": {
            "current_hp": player.current_hp,
            "current_mp": player.current_mp,
            "current_sp": player.current_sp,
        },
        "skills": list(player.skills),
        "skill_cooldowns": deepcopy(player.skill_cooldowns),
        "status_effects": _effect_to_serializable(player.status_effects),
        "active_regen_effects": deepcopy(player.active_regen_effects),
        "inventory": inv,
        "equipment": equipment,
    }


def deserialize_player(player_data):
    base_stats = player_data["base_stats"]
    player = Player(
        name=player_data["name"],
        strength=base_stats["strength"],
        agility=base_stats["agility"],
        vitality=base_stats["vitality"],
        intelligence=base_stats["intelligence"],
        base_atk=player_data["base_atk"],
        base_def=player_data["base_def"],
    )

    player.set_class(player_data["class_name"])

    player.level = int(player_data["level"])
    player.current_xp = int(player_data["current_xp"])
    player.base_stats = deepcopy(base_stats)
    player.strength = base_stats["strength"]
    player.agility = base_stats["agility"]
    player.vitality = base_stats["vitality"]
    player.intelligence = base_stats["intelligence"]
    player.base_atk = player_data["base_atk"]
    player.base_def = player_data["base_def"]
    player.skills = [s.lower() for s in player_data.get("skills", [])]
    player.skill_cooldowns = {k: int(v) for k, v in player_data.get("skill_cooldowns", {}).items()}

    player.inventory.slots = [None] * player.inventory.size
    for idx, item_data in enumerate(player_data.get("inventory", [])):
        if item_data is None:
            continue
        item = create_item(item_data["item_id"])
        item.quantity = int(item_data.get("quantity", 1))
        player.inventory.slots[idx] = item

    for slot_name in player.equipment.slots.keys():
        player.equipment.slots[slot_name] = None

    for slot_name, item_data in player_data.get("equipment", {}).items():
        if item_data is None:
            continue
        item = create_item(item_data["item_id"])
        item.quantity = int(item_data.get("quantity", 1))
        player.equipment.slots[slot_name] = item

    player.status_effects = deepcopy(player_data.get("status_effects", []))
    player.active_regen_effects = deepcopy(player_data.get("active_regen_effects", []))

    player.recalculate_stats()
    player.current_hp = max(1, min(player.max_hp, int(player_data["resources"]["current_hp"])))
    player.current_mp = max(0, min(player.max_mp, int(player_data["resources"]["current_mp"])))
    player.current_sp = max(0, min(player.max_sp, int(player_data["resources"]["current_sp"])))

    return player


def save_run_state(player, current_wave_index, save_type="checkpoint", path=DEFAULT_SAVE_PATH):
    payload = {
        "version": SAVE_VERSION,
        "save_type": save_type,
        "current_wave_index": int(current_wave_index),
        "player": serialize_player(player),
    }

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


def load_run_state(path=DEFAULT_SAVE_PATH):
    path = Path(path)
    if not path.exists():
        return None

    data = json.loads(path.read_text())
    if data.get("version") != SAVE_VERSION:
        raise ValueError("Unsupported save version.")

    player = deserialize_player(data["player"])
    wave_index = int(data.get("current_wave_index", 0))

    return player, wave_index, data
