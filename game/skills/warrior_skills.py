WARRIOR_SKILLS = {

    "slash": {
        "name": "Slash",
        "type": "damage",
        "target": "enemy",
        "cost": {"mp": 0, "sp": 8},
        "cooldown": 1,
        "damage": {
            "flat": 10,
            "scaling": {"strength": 0.6},
            "hits": 1
        },
        "status_effects": [],
        "description": "A basic physical strike."
    },

    "shield_bash": {
        "name": "Shield Bash",
        "type": "damage",
        "target": "enemy",
        "cost": {"mp": 0, "sp": 12},
        "cooldown": 2,
        "damage": {
            "flat": 6,
            "scaling": {"strength": 0.4},
            "hits": 1
        },
        "status_effects": [
            {"name": "Stun", "duration": 1}
        ],
        "description": "A bash that deals damage and may stun the target."
    },

    "iron_skin": {
        "name": "Iron Skin",
        "type": "buff",
        "target": "self",
        "cost": {"mp": 0, "sp": 10},
        "cooldown": 3,
        "status_effects": [
            {
                "name": "BuffDefense",
                "duration": 3,
                "data": {"percent": 0.20}
            }
        ],
        "description": "Increase your Defense by 20% for 3 turns."
    },

    "battle_cry": {
        "name": "Battle Cry",
        "type": "buff",
        "target": "self",
        "cost": {"mp": 0, "sp": 10},
        "cooldown": 3,
        "status_effects": [
            {
                "name": "AttackUp",
                "duration": 3,
                "data": {"flat": 5}
            }
        ],
        "description": "Boost your Attack by 5 for 3 turns."
    },

    "whirlwind": {
        "name": "Whirlwind",
        "type": "aoe",
        "target": "all_enemies",
        "cost": {"mp": 0, "sp": 15},
        "cooldown": 3,
        "damage": {
            "flat": 7,
            "scaling": {"strength": 0.4},
            "hits": 1
        },
        "status_effects": [],
        "description": "Spin and strike all enemies."
    },

    "execution": {
        "name": "Execution",
        "type": "ultimate",
        "target": "enemy",
        "cost": {"mp": 0, "sp": 20},
        "cooldown": 5,
        "damage": {
            "flat": 20,
            "scaling": {"strength": 1.0},
            "hits": 1
        },
        "status_effects": [],
        "description": "A devastating finishing blow."
    }
}
