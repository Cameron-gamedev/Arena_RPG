import random
from game.status.status_definitions import STATUS_DEFINITIONS


def _resolve_target(source, target_group, se):
    # Default: hit the enemy or player directly
    target = target_group.get("default")

    # Self-targeting
    if se.get("target") == "self":
        return source

    # Ally targeting (lowest HP %)
    if se.get("target") == "ally":
        allies = target_group.get("allies", [])
        allies = [a for a in allies if not a.is_dead() and a is not source]
        if allies:
            return min(allies, key=lambda a: a.current_hp / a.max_hp)

    # Enemy targeting (lowest HP %)
    if se.get("target") == "enemy":
        enemies = target_group.get("enemies", [])
        enemies = [e for e in enemies if not e.is_dead()]
        if enemies:
            return min(enemies, key=lambda e: e.current_hp / e.max_hp)

    return target




def apply_status_effects(source, target_group, effect_list, hit_landed=True):
    """
    source: the entity applying the effect
    target_group: dict with keys:
        - "player": player entity
        - "enemies": list of enemies
        - "self": source entity
    effect_list: list of status effect dicts from skills/actions
    hit_landed: whether the damage portion hit (for damage-based effects)
    """

    if not effect_list:
        return

    for se in effect_list:
        definition = STATUS_DEFINITIONS[se["name"]]

        # Respect chance
        effect_chance = se.get("chance", definition.get("chance", 1.0))
        if random.random() > effect_chance:
            continue

        # Skip if damage-based and hit missed
        if se.get("requires_hit", False) and not hit_landed:
            continue

        # Determine target
        target = _resolve_target(source, target_group, se)

        # Apply status to target
        data = dict(se.get("data", {}))
        data["applier"] = source   # <--- store the actual enemy object

        target.apply_status(
            name=se["name"],
            effect_type=definition["type"],
            duration=se["duration"],
            data=data
        )

        # Optional: stun chance baked into definition
        if "stun_chance" in definition:
            if random.random() < definition["stun_chance"]:
                target.apply_status("Stun", "stun", 1, {})
