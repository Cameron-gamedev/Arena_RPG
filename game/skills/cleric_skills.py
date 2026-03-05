CLERIC_SKILLS = {

    "smite": {
        "name": "Smite",
        "type": "damage",
        "target": "enemy",
        "cost": {"mp": 6, "sp": 0},
        "cooldown": 1,
        "damage": {
            "flat": 10,
            "scaling": {"intelligence": 0.5},
            "hits": 1
        },
        "status_effects": [],
        "description": "A holy strike of radiant energy."
    },

    "heal": {
        "name": "Heal",
        "type": "heal",
        "target": "ally",
        "cost": {"mp": 10, "sp": 0},
        "cooldown": 2,
        "healing": {
            "flat": 12,
            "scaling": {"intelligence": 0.8}
        },
        "status_effects": [],
        "description": "Restore health to an ally."
    },

    "bless": {
        "name": "Bless",
        "type": "buff",
        "target": "ally",
        "cost": {"mp": 8, "sp": 0},
        "cooldown": 3,
        "status_effects": [
            {
                "name": "BuffDefenseFlat",
                "duration": 3,
                "data": {"flat": 5}
            }
        ],
        "description": "Increase an ally's Defense by 5 for 3 turns."
    },

    "holy_nova": {
        "name": "Holy Nova",
        "type": "aoe",
        "target": "all_enemies",
        "cost": {"mp": 12, "sp": 0},
        "cooldown": 3,
        "damage": {
            "flat": 8,
            "scaling": {"intelligence": 0.5},
            "hits": 1
        },
        "status_effects": [],
        "description": "A burst of holy energy that damages all enemies."
    },

    "divine_judgment": {
        "name": "Divine Judgment",
        "type": "ultimate",
        "target": "enemy",
        "cost": {"mp": 18, "sp": 0},
        "cooldown": 5,
        "damage": {
            "flat": 22,
            "scaling": {"intelligence": 1.0},
            "hits": 1
        },
        "status_effects": [],
        "description": "Call down divine wrath upon a single foe."
    }
}
