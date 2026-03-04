WAVE_DEFINITIONS = [

    # -------------------------
    # Goblin Tier (1–4)
    # -------------------------
    {
        "wave": 1,
        "tier": "goblin",
        "enemies": [
            {"type": "Goblin Skirmisher", "elite": False, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.0,
        "loot_table": "early",
        "event": None
    },

    {
        "wave": 2,
        "tier": "goblin",
        "enemies": [
            {"type": "Goblin Skirmisher", "elite": False, "boss": False},
            {"type": "Goblin Assassin", "elite": False, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.05,
        "loot_table": "early",
        "event": None
    },

    {
        "wave": 3,
        "tier": "goblin",
        "enemies": [
            {"type": "Goblin Saboteur", "elite": False, "boss": False},
            {"type": "Goblin Shaman", "elite": False, "boss": False},
            {"type": "Shadowblade Saboteur", "elite": True, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.1,
        "loot_table": "early",
        "event": None
    },

    {
        "wave": 4,
        "tier": "goblin",
        "enemies": [
            {"type": "Goblin Warlock-King", "elite": True, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.25,
        "loot_table": "early",
        "event": "goblin_boss_intro"
    },

    # -------------------------
    # Orc Tier (5–8)
    # -------------------------
    {
        "wave": 5,
        "tier": "orc",
        "enemies": [
            {"type": "Orc Grunt", "elite": False, "boss": False},
            {"type": "Orc Grunt", "elite": False, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.15,
        "loot_table": "midgame",
        "event": None
    },

    {
        "wave": 6,
        "tier": "orc",
        "enemies": [
            {"type": "Orc Brute", "elite": False, "boss": False},
            {"type": "Orc Warcaller", "elite": False, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.2,
        "loot_table": "midgame",
        "event": None
    },

    {
        "wave": 7,
        "tier": "orc",
        "enemies": [
            {"type": "Orc Grunt", "elite": False, "boss": False},
            {"type": "Orc Berserker", "elite": False, "boss": False},
            {"type": "Orc Ironbreaker Champion", "elite": True, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.3,
        "loot_table": "midgame",
        "event": None
    },

    {
        "wave": 8,
        "tier": "orc",
        "enemies": [
            {"type": "Orc Doomcaller Warlord", "elite": False, "boss": True}
        ],
        "forced_modifiers": ["OrcFury"],
        "xp_multiplier": 1.5,
        "loot_table": "boss",
        "event": "orc_boss_intro"
    },

    # -------------------------
    # Troll Tier (9–13)
    # -------------------------
    {
        "wave": 9,
        "tier": "troll",
        "enemies": [
            {"type": "Troll Bruiser", "elite": False, "boss": False},
            {"type": "Troll Regenerator", "elite": False, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.35,
        "loot_table": "lategame",
        "event": None
    },

    {
        "wave": 10,
        "tier": "troll",
        "enemies": [
            {"type": "Troll Firebelly", "elite": False, "boss": False},
            {"type": "Troll Shaman", "elite": False, "boss": False},
            {"type": "Troll Boulderback Crusher", "elite": True, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.45,
        "loot_table": "lategame",
        "event": None
    },

    {
        "wave": 11,
        "tier": "troll",
        "enemies": [
            {"type": "Troll Bruiser", "elite": False, "boss": False},
            {"type": "Troll Shaman", "elite": False, "boss": False},
            {"type": "Troll Volcanic Devourer", "elite": False, "boss": True}
        ],
        "forced_modifiers": ["RegenerationAura"],
        "xp_multiplier": 1.6,
        "loot_table": "boss",
        "event": "troll_boss_intro"
    },

    {
        "wave": 12,
        "tier": "troll",
        "enemies": [
            {"type": "Troll Regenerator", "elite": False, "boss": False},
            {"type": "Troll Firebelly", "elite": False, "boss": False},
            {"type": "Troll Boulderback Crusher", "elite": True, "boss": False}
        ],
        "forced_modifiers": [],
        "xp_multiplier": 1.7,
        "loot_table": "lategame",
        "event": None
    },

    {
        "wave": 13,
        "tier": "troll",
        "enemies": [
            {"type": "Troll Volcanic Devourer", "elite": False, "boss": True}
        ],
        "forced_modifiers": ["BurningGround", "SpiritDrain"],
        "xp_multiplier": 2.0,
        "loot_table": "final_boss",
        "event": "finale"
    }
]
