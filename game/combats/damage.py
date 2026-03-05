# game/combats/damage.py

import math
import random


def calculate_damage(attacker, defender, skill=None):
    """
    Unified damage function for:
    - basic attacks  (skill=None)
    - skills         (skill is a dict with optional 'damage' block)
    """

    # -------------------------
    # 1. Accuracy vs Dodge (ratio-based, clamped)
    # -------------------------
    att_hit = max(0.05, min(0.95, getattr(attacker, "hit_chance", 0.75)))
    def_dodge = max(0.00, min(0.95, getattr(defender, "dodge_chance", 0.0)))

    total = att_hit + def_dodge
    effective_hit = att_hit / total if total > 0 else att_hit
    effective_hit = max(0.05, min(0.95, effective_hit))

    if random.random() > effective_hit:
        # miss
        return 0, False, True

    # -------------------------
    # 2. Base damage (attack + optional skill scaling)
    # -------------------------
    base_damage = getattr(attacker, "attack", 0)

    if skill is not None:
        dmg_info = skill.get("damage", {})

        # Flat bonus
        flat = dmg_info.get("flat", 0)
        base_damage += flat

        # Scaling bonus
        scaling = dmg_info.get("scaling", {})
        for stat_name, factor in scaling.items():
            if hasattr(attacker, "get_scaled_stat"):
                final_attr = attacker.get_scaled_stat(stat_name)
            else:
                final_attr = getattr(attacker, stat_name.lower(), 0)
            base_damage += final_attr * factor

    # -------------------------
    # 3. Softer defense curve (shared for physical & magical)
    # mitigation = DEF / (DEF + 100)
    # -------------------------
    defense = getattr(defender, "defense", 0)
    mitigation = defense / (defense + 100) if defense > 0 else 0.0
    mitigation = max(0.0, min(0.8, mitigation))  # optional cap

    damage_after_def = base_damage * (1 - mitigation)

    # -------------------------
    # 4. Flat armor mitigation
    # -------------------------
    armor_defense = getattr(defender, "armor_defense", 0)
    damage_after_flat = damage_after_def - armor_defense

    # -------------------------
    # 5. Variance (±10%) AFTER mitigation
    # -------------------------
    variance = random.uniform(0.9, 1.1)
    damage_after_var = damage_after_flat * variance

    # -------------------------
    # 6. Crit AFTER mitigation + variance
    # -------------------------
    crit_chance = getattr(attacker, "crit_chance", 0.05)
    is_crit = random.random() < crit_chance
    if is_crit:
        damage_after_var *= 1.5

    # -------------------------
    # 7. Clamp + ceil
    # -------------------------
    final_damage = max(1, math.ceil(damage_after_var))

    return final_damage, is_crit, False
