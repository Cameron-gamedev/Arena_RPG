
import random
from game.modifiers.modifier_definitions import MODIFIER_DEFINITIONS
from game.modifiers.modifier_pools import MODIFIER_POOLS


def roll_modifiers(tier):
    pool = MODIFIER_POOLS.get(tier, [])
    count = random.choice([0, 1, 1, 2])  # weighted: 50% 1 mod, 25% 0, 25% 2
    return random.sample(pool, min(count, len(pool)))


def apply_modifiers(modifier_ids, engine, enemies, player):
    for mod_id in modifier_ids:
        definition = MODIFIER_DEFINITIONS.get(mod_id)
        if definition:
            definition["apply"](engine, enemies, player)


def display_modifiers(modifier_ids):
    if not modifier_ids:
        print("No wave modifiers this round.")
        return

    print("\n— Wave Modifiers —")
    for mod_id in modifier_ids:
        desc = MODIFIER_DEFINITIONS[mod_id]["description"]
        print(f"• {mod_id}: {desc}")
