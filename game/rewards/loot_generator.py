import random
from game.items.item_factory import create_item
from game.rewards.loot_tables import LOOT_TABLES

RARITY_WEIGHTS = {
    "common": 70,
    "uncommon": 20,
    "rare": 8,
    "epic": 2
}

def choose_rarity(force_rare=False):
    if force_rare:
        return random.choice(["rare", "epic"])
    rarities = list(RARITY_WEIGHTS.keys())
    weights = list(RARITY_WEIGHTS.values())
    return random.choices(rarities, weights=weights, k=1)[0]


def roll_item_from_pool(pool):
    if not pool:
        return None
    return create_item(random.choice(pool))


def roll_loot(loot_table_id, player_class, force_rare=False):
    table = LOOT_TABLES[loot_table_id]

    rarity = choose_rarity(force_rare)
    pool = table[rarity]

    # 70% chance to use class-specific pool if available
    class_pool = table.get("class_specific", {}).get(player_class, [])
    if class_pool and random.random() < 0.7:
        return roll_item_from_pool(class_pool)

    return roll_item_from_pool(pool)


def generate_wave_loot(loot_table_id, player_class, is_boss_wave=False):
    drops = []

    num_items = random.choice([1, 1, 2, 3])

    # Boss guarantee: first item is Rare/Epic
    if is_boss_wave:
        guaranteed = roll_loot(loot_table_id, player_class, force_rare=True)
        if guaranteed:
            drops.append(guaranteed)
        num_items -= 1

    # Roll remaining items normally
    for _ in range(num_items):
        item = roll_loot(loot_table_id, player_class)
        if item:
            drops.append(item)

    return drops
