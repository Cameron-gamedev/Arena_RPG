WIZARD_SKILLS = {

    "magic_bolt": {
        "name": "Magic Bolt",
        "type": "damage",
        "target": "enemy",
        "cost": {"mp": 8, "sp": 0},
        "cooldown": 1,
        "damage": {
            "flat": 12,
            "scaling": {"intelligence": 0.7},
            "hits": 1
        },
        "status_effects": [],
        "description": "A focused burst of arcane energy."
    },

    "ignite": {
        "name": "Ignite",
        "type": "dot",
        "target": "enemy",
        "cost": {"mp": 10, "sp": 0},
        "cooldown": 2,
        "status_effects": [
            {
                "name": "Burn",
                "duration": 3,
                "data": {"amount_per_turn": 6}
            }
        ],
        "description": "Ignites the target, dealing fire damage over time."
    },

    "frost_nova": {
        "name": "Frost Nova",
        "type": "aoe",
        "target": "all_enemies",
        "cost": {"mp": 14, "sp": 0},
        "cooldown": 3,
        "damage": {
            "flat": 8,
            "scaling": {"intelligence": 0.5},
            "hits": 1
        },
        "status_effects": [
            {
                "name": "Slow",
                "duration": 2,
                "data": {"percent": -0.20}
            }
        ],
        "description": "A burst of frost that damages and slows all enemies."
    },

    "arcane_surge": {
        "name": "Arcane Surge",
        "type": "buff",
        "target": "self",
        "cost": {"mp": 12, "sp": 0},
        "cooldown": 4,
        "status_effects": [
            {
                "name": "BuffSpellPower",
                "duration": 3,
                "data": {"percent": 0.25}
            }
        ],
        "description": "Increase spell power by 25% for 3 turns."
    },

    "meteor": {
        "name": "Meteor",
        "type": "ultimate",
        "target": "all_enemies",
        "cost": {"mp": 20, "sp": 0},
        "cooldown": 6,
        "damage": {
            "flat": 25,
            "scaling": {"intelligence": 1.2},
            "hits": 1
        },
        "status_effects": [
            {
                "name": "Burn",
                "duration": 3,
                "data": {"amount_per_turn": 8}
            }
        ],
        "description": "Call down a massive meteor to devastate all enemies."
    }
}
