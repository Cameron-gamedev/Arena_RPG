def accumulate_status_modifiers(entity, base_stats):
    """
    Reads entity.status_effects and produces a dict:
    {
        stat_name: { "flat": X, "percent": Y }
    }
    """
    from game.status.status_definitions import STATUS_DEFINITIONS

    modifiers = {}

    for effect in entity.status_effects:
        name = effect["name"]
        definition = STATUS_DEFINITIONS[name]
        data = effect.get("data", {})

        stat = definition.get("stat")
        if not stat:
            continue

        # Ensure entry exists
        if stat not in modifiers:
            modifiers[stat] = {"flat": 0, "percent": 0}

        # Buffs
        if definition["type"] == "buff":
            modifiers[stat]["flat"] += data.get("flat", 0)
            modifiers[stat]["percent"] += data.get("percent", 0)

        # Debuffs
        elif definition["type"] == "debuff":
            modifiers[stat]["flat"] += data.get("flat", 0)
            modifiers[stat]["percent"] += definition.get("percent", 0)

            # Special fields (e.g., hit chance penalty)
            if "hit_chance_penalty" in definition:
                if "hit_chance" not in modifiers:
                    modifiers["hit_chance"] = {"flat": 0, "percent": 0}
                modifiers["hit_chance"]["flat"] += definition["hit_chance_penalty"]

    return modifiers
