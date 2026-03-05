ITEM_DEFINITIONS = {

    # ============================================================
    # WEAPONS
    # ============================================================
    "iron_sword": {
        "name": "Iron Sword",
        "item_type": "weapon",
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 5,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {
            "flat": {},
            "percent": {}
        }
    },

    # ============================================================
    # ARMOR
    # ============================================================
    "leather_armor": {
        "name": "Leather Armor",
        "item_type": "armor",
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 3,
        "crit_bonus": 0,
        "modifiers": {
            "flat": {},
            "percent": {}
        }
    },

    "wooden_shield": {
        "name": "Wooden Shield",
        "item_type": "shield",
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 2,
        "crit_bonus": 0,
        "modifiers": {
            "flat": {},
            "percent": {}
        }
    },

    # ============================================================
    # ACCESSORIES
    # ============================================================
    "simple_ring": {
        "name": "Simple Ring",
        "item_type": "ring",
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0.02,   # +2% crit
        "modifiers": {
            "flat": {},
            "percent": {}
        }
    },

    "basic_amulet": {
        "name": "Basic Amulet",
        "item_type": "amulet",
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0.01,   # +1% crit
        "modifiers": {
            "flat": {},
            "percent": {}
        }
    },

    # ============================================================
    # STAT-MODIFYING EQUIPMENT
    # ============================================================
    "belt_of_strength": {
        "name": "Belt of Strength",
        "item_type": "armor",
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {
            "flat": {"strength": 2},
            "percent": {}
        }
    },

    "warriors_charm": {
        "name": "Warrior's Charm",
        "item_type": "amulet",
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {
            "flat": {},
            "percent": {"attack": 0.10}   # +10% attack
        }
    },

    "champions_gauntlets": {
        "name": "Champion's Gauntlets",
        "item_type": "armor",
        "stackable": False,
        "quantity": 1,
        "attack_bonus": 0,
        "defense_bonus": 1,
        "crit_bonus": 0,
        "modifiers": {
            "flat": {"strength": 5},
            "percent": {"attack": 0.05}   # +5% attack
        }
    },

    # ============================================================
    # CONSUMABLES — INSTANT HEAL
    # ============================================================
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
        "modifiers": {
            "flat": {},
            "percent": {}
        }
    },

    # ============================================================
    # CONSUMABLES — REGEN OVER TIME
    # ============================================================
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
        "modifiers": {
            "flat": {},
            "percent": {}
        }
    },

    # ============================================================
    # CONSUMABLES — BUFFS (NOW USING STATUS EFFECTS)
    # ============================================================
    "strength_elixir": {
        "name": "Elixir of Strength",
        "item_type": "consumable",
        "stackable": False,
        "quantity": 1,
        "effect": {
            "kind": "status",
            "status_name": "BuffStrength",
            "duration": 3,
            "data": {"percent": 0.20}   # +20% STR
        },
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {
            "flat": {},
            "percent": {}
        }
    },

    # ============================================================
    # CONSUMABLES — DAMAGE OVER TIME
    # ============================================================
    "poison_bomb": {
        "name": "Poison Bomb",
        "item_type": "consumable",
        "stackable": True,
        "quantity": 1,
        "effect": {
            "kind": "status",
            "status_name": "Poison",
            "duration": 3,
            "data": {"amount_per_turn": 4}
        },
        "attack_bonus": 0,
        "defense_bonus": 0,
        "crit_bonus": 0,
        "modifiers": {
            "flat": {},
            "percent": {}
        }
    },
}
