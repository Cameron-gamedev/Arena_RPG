STATUS_DEFINITIONS = {

    # ============================
    # HEAL OVER TIME (HOT)
    # ============================
    "RegenHP": {"type": "hot", "target": "hp", "stacking": "stack"},
    "RegenMP": {"type": "hot", "target": "mp", "stacking": "stack"},
    "RegenSP": {"type": "hot", "target": "sp", "stacking": "stack"},

    # ============================
    # DAMAGE OVER TIME (DOT)
    # ============================
    "Poison": {"type": "dot", "target": "hp", "stacking": "stack"},
    "Burn":   {"type": "dot", "target": "hp", "stacking": "stack"},
    "Bleed":  {"type": "dot", "target": "hp", "stacking": "stack"},

    # ============================
    # ATTRIBUTE BUFFS
    # ============================
    "BuffStrength":     {"type": "buff", "stat": "strength",     "stacking": "refresh"},
    "BuffAgility":      {"type": "buff", "stat": "agility",      "stacking": "refresh"},
    "BuffVitality":     {"type": "buff", "stat": "vitality",     "stacking": "refresh"},
    "BuffIntelligence": {"type": "buff", "stat": "intelligence", "stacking": "refresh"},
    "BuffDodgeChance":  {"type": "buff", "stat": "dodge_chance", "stacking": "refresh"},

    # ============================
    # COMBAT BUFFS (Orc + General)
    # ============================
    "BattleFury":     {"type": "buff", "stat": "attack",      "flat": 0,    "percent": 0.20, "stacking": "refresh"},
    "Rage":           {"type": "buff", "stat": "attack",      "flat": 0,    "percent": 0.25, "stacking": "ignore"},
    "Warcry":         {"type": "buff", "stat": "attack",      "flat": 0,    "percent": 0.15, "stacking": "refresh"},
    "BattleRhythm":   {"type": "buff", "stat": "sp_regen",    "flat": 1,    "percent": 0.00, "stacking": "refresh"},
    "DrumsOfBattle":  {"type": "buff", "stat": "sp_regen",    "flat": 1,    "percent": 0.00, "stacking": "refresh"},
    "BuffCritChance": {"type": "buff", "stat": "crit_chance", "flat": 0.10, "percent": 0.00, "stacking": "refresh"},
    "BuffHitChance":  {"type": "buff", "stat": "hit_chance",  "flat": 0.10, "percent": 0.00, "stacking": "refresh"},

    # ============================
    # DEBUFFS
    # ============================
    "Weaken":        {"type": "debuff", "stat": "attack",        "percent": -0.10, "stacking": "refresh"},
    "Vulnerable":    {"type": "debuff", "stat": "defense",       "percent": -0.25, "stacking": "refresh"},
    "Slow":          {"type": "debuff", "stat": "agility",       "percent": -0.20, "stacking": "refresh"},
    "AccuracyDown":  {"type": "debuff", "stat": "hit_chance",    "percent": -0.20, "stacking": "refresh", "chance": 0.25},
    "GuardBreak":    {"type": "debuff", "stat": "defense",       "percent": -0.20, "stacking": "refresh"},
    "ArmorShatter":  {"type": "debuff", "stat": "armor_defense", "flat": -1,       "stacking": "refresh"},
    "Intimidate":    {"type": "debuff", "stat": "hit_chance",    "percent": -0.10, "stacking": "refresh"},
    "CritDown":      {"type": "debuff", "stat": "crit_chance",   "percent": -0.10, "stacking": "refresh"},

    # ============================
    # CROWD CONTROL & SPECIAL
    # ============================
    "Stun":    {"type": "stun", "stacking": "refresh"},
    "Stagger": {"type": "debuff", "stat": "sp_regen", "percent": -1.00,"stacking": "refresh", "hit_chance_penalty": -0.10},
    "Shock":   {"type": "debuff", "stat": "defense",  "percent": -0.10,"stacking": "refresh", "stun_chance": 0.20}
}