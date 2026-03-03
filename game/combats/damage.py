
def calculate_damage(attacker, defender, skill=None):
    import math
    import random

    # -------------------------
    # 1. Accuracy vs Dodge (ratio-based, clamped)
    # -------------------------
    att_hit = max(0.05, min(0.95, attacker.hit_chance))
    def_dodge = max(0.00, min(0.95, defender.dodge_chance))

    total = att_hit + def_dodge
    effective_hit = att_hit / total

    # Final clamp
    effective_hit = max(0.05, min(0.95, effective_hit))

    if random.random() > effective_hit:
        return 0, False, True
    
    # -------------------------
    # 2. Crit Check 
    # ------------------------- 
    crit_roll = random.random()
    is_crit = crit_roll < attacker.crit_chance

    base_damage = attacker.attack
    
    if skill is not None:
        dmg_info = skill.get("damage", {})

        # Flat bonus
        flat = dmg_info.get("flat", 0)
        base_damage += flat

        # Scaling bonus
        scaling = dmg_info.get("scaling", {})
        for stat_name, factor in scaling.items():
            stat_value = getattr(attacker, stat_name, 0)
            base_damage += stat_value * factor

    if is_crit:
        base_damage = int(base_damage * 1.5)

    # -------------------------
    # 3. Percent Mitigation
    # -------------------------
    base_defense = getattr(defender, "base_def", defender.defense)
    percent = base_defense * 0.01
    percent = min(percent, 0.80)

    damage_after_percent = base_damage * (1 - percent)

    # -------------------------
    # 4. Flat Mitigation
    # -------------------------
    armor_defense = getattr(defender, "armor_defense", 0)
    damage_after_flat = damage_after_percent - armor_defense

    # -------------------------
    # 5. Clamp + Ceil
    # -------------------------
    final_damage = max(1, math.ceil(damage_after_flat))

    return final_damage, is_crit, False
