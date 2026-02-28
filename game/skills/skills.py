SKILLS_DB = {
    "Fireball": {
        "name": "Fireball",
        "description": "Hurl a ball of fire at one enemy.",
        "target": "enemy",
        "cost_type":"mp",
        "cost": 8,
        "cooldown":0, # basic or mid-tier → no cooldown
        "damage": {
            "flat": 5,
            "scaling": {"intelligence": 1.0},
            "hits": 1
        },
        "status_effects":[
            {"name":"Weaken", "duration":2},
            {"name":"Stun", "duration": 1}
        ]
    },

    "Cleave": {
        "name": "Cleave",
        "description": "Swing your weapon in a wide arc, hitting all enemies.",
        "target": "all_enemies",
        "cost_type":"sp",
        "cost": 12,
        "cooldown":0, # basic or mid-tier → no cooldown
        "damage": {
            "flat": 3,
            "scaling": {"strength": 0.5},
            "hits": 1
        },
        "status_effects":[
            {"name":"Weaken", "duration":2},
            {"name":"Stun", "duration": 1}
        ]
    },

    "ArcaneNova": {
        "name": "Arcane Nova",
        "description": "Unleash a devastating blast of arcane energy.",
        "target": "all_enemies",
        "cost_type": "mp",
        "cost": 25,
        "cooldown": 4,   # ultimate → cooldown
        "damage": {
            "flat": 10,
            "scaling": {"intelligence": 1.5},
            "hits": 1
        }
    },

    "toxic_strike": {
        "name": "Toxic Strike",
        "description": "Deal damage and apply poison.",
        "target": "enemy",
        "damage": {
            "flat": 8,
            "scaling": {"strength": 0.4},
            "hits": 1
        },
        "status_effects": [
            {
                "name": "Poison",
                "duration": 3,
                "amount_per_turn": 5
            }
        ],
        "cost_type": "sp",
        "cost": 10,
        "cooldown": 2
    }



}
