RANGER_SKILLS = {

    "quick_shot": {
        "name": "Quick Shot",
        "type": "damage",
        "target": "enemy",
        "cost": {"mp": 0, "sp": 6},
        "cooldown": 1,
        "damage": {
            "flat": 8,
            "scaling": {"agility": 0.5},
            "hits": 1
        },
        "status_effects": [],
        "description": "A fast, precise arrow shot."
    },

    "poison_arrow": {
        "name": "Poison Arrow",
        "type": "dot",
        "target": "enemy",
        "cost": {"mp": 0, "sp": 10},
        "cooldown": 2,
        "status_effects": [
            {
                "name": "Poison",
                "duration": 3,
                "data": {"amount_per_turn": 5}
            }
        ],
        "description": "Applies poison that deals damage over time."
    },

    "multi_shot": {
        "name": "Multi Shot",
        "type": "multi_hit",
        "target": "enemy",
        "cost": {"mp": 0, "sp": 12},
        "cooldown": 3,
        "damage": {
            "flat": 5,
            "scaling": {"agility": 0.3},
            "hits": 3
        },
        "status_effects": [],
        "description": "Fire multiple arrows at a single target."
    },

    "eagle_eye": {
        "name": "Eagle Eye",
        "type": "buff",
        "target": "self",
        "cost": {"mp": 0, "sp": 10},
        "cooldown": 4,
        "status_effects": [
            {
                "name": "BuffCritChance",
                "duration": 3,
                "data": {"percent": 0.15}
            }
        ],
        "description": "Increase critical chance by 15% for 3 turns."
    },

    "rain_of_arrows": {
        "name": "Rain of Arrows",
        "type": "ultimate",
        "target": "all_enemies",
        "cost": {"mp": 0, "sp": 18},
        "cooldown": 5,
        "damage": {
            "flat": 10,
            "scaling": {"agility": 0.6},
            "hits": 1
        },
        "status_effects": [
            {
                "name": "Bleed",
                "duration": 3,
                "data": {"amount_per_turn": 4}
            }
        ],
        "description": "Unleash a volley of arrows on all enemies."
    }
}
