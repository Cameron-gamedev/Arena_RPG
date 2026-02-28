
ITEM_DEFINITIONS = {

    "iron_sword": {
        "name": "Iron Sword",
        "item_type": "weapon",
        "effect": None,
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 5,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {}
    },

    "leather_armor": {
        "name": "Leather Armor",
        "item_type": "armor",
        "effect": None,
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 3,
        "crit_bonus": 0,
        "modifiers": {}
    },

    "simple_ring": {
        "name": "Simple Ring",
        "item_type": "ring",
        "effect": None,
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0.02,   # +2% crit
        "modifiers": {}
    },

    "basic_amulet": {
        "name": "Basic Amulet",
        "item_type": "amulet",
        "effect": None,
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0.01,   # +1% crit
        "modifiers": {}
    },

    "wooden_shield": {
        "name": "Wooden Shield",
        "item_type": "shield",
        "effect": None,
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 2,
        "crit_bonus": 0,
        "modifiers": {}
    },

    "belt_of_strength": {
        "name": "Belt of Strength",
        "item_type": "armor",   # or "accessory" if you add belts later
        "effect": None,
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {
            "strength": {"value": 2, "is_percent": False}
        }
    },
    
    # Percent‑modifier Items
    "warriors_charm": {
        "name": "Warrior's Charm",
        "item_type": "amulet",
        "effect": None,
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {
            "attack": {"value": 0.10, "is_percent": True}
        }
    },

    "champions_gauntlets": {
        "name": "Champion's Gauntlets",
        "item_type": "armor",
        "effect": None,
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 1,
        "crit_bonus": 0,
        "modifiers": {
            "strength": {"value": 5, "is_percent": False},
            "attack": {"value": 0.05, "is_percent": True}
        }
    },
    
    # Consumable Items
    "minor_health_potion": {
        "name": "Minor Health Potion",
        "item_type": "consumable",
        "stackable": True,
        "quantity": 1,
        "effect": {
            "kind": "restore_instant",
            "target": "hp",
            "percent": 0.30
        },
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {}
    },

    "rejuvenation_potion": {
        "name": "Rejuvenation Potion",
        "item_type": "consumable",
        "stackable": True,
        "quantity": 1,
        "effect": {
            "kind": "restore_over_time",
            "target": "hp",
            "percent": 0.40,
            "duration": 3
        },
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {}
    },

    "strength_elixir": {
        "name": "Elixir of Strength",
        "item_type": "consumable",
        "stackable": False,
        "quantity": 1,
        "effect": {
            "kind": "buff",
            "stat": "strength",
            "percent": 0.20,
            "duration": 3
        },
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {}
    },

    #Attack Items
    "poison_bomb": {
        "name": "Poison Bomb",
        "item_type": "consumable",
        "stackable": True,
        "quantity": 1,
        "effect": {
            "kind": "status",
            "status_name": "Poison",
            "duration": 3,
            "amount_per_turn": 4
        },
    },
}
