CLASS_DEFINITIONS = {
    "Warrior": {
        "base_stats": {"strength": 5, "agility": 2, "vitality": 6, "intelligence": 1},
        "growth": {"strength": 3, "agility": 1, "vitality": 3, "intelligence": 0},
        "resources": {"hp_per_level": 20, "mp_per_level": 2, "sp_per_level": 8},
        "regen": {"hp": 1, "mp": 0, "sp": 3},
        "between_wave_regen": {"hp_percent": 0.30, "mp_percent": 0.10, "sp_percent": 0.80},
        "passives": {"armor_bonus": 2},
        "skills": {
            1: ["Slash"],
            3: ["ShieldBash"],
            5: ["BattleCry"],
            8: ["Whirlwind"],
            12: ["Execution"]
        }
    },

    "Wizard": {
        "base_stats": {"strength": 1, "agility": 2, "vitality": 2, "intelligence": 7},
        "growth": {"strength": 0, "agility": 1, "vitality": 1, "intelligence": 4},
        "resources": {"hp_per_level": 10, "mp_per_level": 12, "sp_per_level": 2},
        "regen": {"hp": 0, "mp": 3, "sp": 1},
        "between_wave_regen": {"hp_percent": 0.10, "mp_percent": 0.80, "sp_percent": 0.20},
        "passives": {"spell_power_scaling": 0.20},
        "skills": {
            1: ["MagicBolt"],
            2: ["Ignite"],
            4: ["FrostNova"],
            7: ["ArcaneSurge"],
            12: ["Meteor"]
        }
    },

    "Ranger": {
        "base_stats": {"strength": 3, "agility": 6, "vitality": 3, "intelligence": 2},
        "growth": {"strength": 1, "agility": 3, "vitality": 1, "intelligence": 1},
        "resources": {"hp_per_level": 15, "mp_per_level": 5, "sp_per_level": 5},
        "regen": {"hp": 0, "mp": 1, "sp": 2},
        "between_wave_regen": {"hp_percent": 0.20, "mp_percent": 0.40, "sp_percent": 0.40},
        "passives": {"crit_bonus": 0.05, "dodge_bonus": 0.05},
        "skills": {
            1: ["QuickShot"],
            3: ["PoisonArrow"],
            6: ["MultiShot"],
            10: ["EagleEye"],
            12: ["RainOfArrows"]
        }
    },

    "Cleric": {
        "base_stats": {"strength": 2, "agility": 2, "vitality": 5, "intelligence": 5},
        "growth": {"strength": 1, "agility": 1, "vitality": 2, "intelligence": 2},
        "resources": {"hp_per_level": 18, "mp_per_level": 8, "sp_per_level": 3},
        "regen": {"hp": 1, "mp": 2, "sp": 1},
        "between_wave_regen": {"hp_percent": 0.25, "mp_percent": 0.60, "sp_percent": 0.20},
        "passives": {"healing_power": 0.15},
        "skills": {
            1: ["Smite"],
            2: ["Heal"],
            4: ["Bless"],
            7: ["HolyNova"],
            12: ["DivineJudgment"]
        }
    }
}
