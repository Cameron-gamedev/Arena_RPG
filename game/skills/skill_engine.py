# game/skills/skill_engine.py

from game.combats.damage import calculate_damage
from game.status.status_definitions import STATUS_DEFINITIONS


# ============================================================
# TARGETING HELPERS
# ============================================================

def prompt_player_for_enemy_target(enemies):
    living = [e for e in enemies if not e.is_dead()]
    if not living:
        return None

    print("\nChoose a target:")
    for i, e in enumerate(living, start=1):
        print(f"{i}. {e.name} {e.current_hp}/{e.max_hp} HP")

    choice = input("Target number: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(living):
            return living[idx]

    print("Invalid choice.")
    return None


def auto_target_lowest_hp(allies):
    living = [a for a in allies if not a.is_dead()]
    if not living:
        return None
    return min(living, key=lambda a: a.current_hp / a.max_hp)


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def execute_skill(user, skill_id, enemies, allies=None):
    """
    allies: list of friendly units (for future party support)
    enemies: list of enemy units
    """

    from game.skills.skill_loader import ALL_SKILLS
    skill = ALL_SKILLS[skill_id]

    # -------------------------
    # Cooldown + resource checks
    # -------------------------
    remaining = user.skill_cooldowns.get(skill_id, 0)
    if remaining > 0:
        print(f"{skill['name']} is on cooldown for {remaining} more turn(s)!")
        return "cancel"

    cost_mp = skill["cost"].get("mp", 0)
    cost_sp = skill["cost"].get("sp", 0)

    if user.current_mp < cost_mp or user.current_sp < cost_sp:
        print(f"{user.name} does not have enough resources to use {skill['name']}!")
        return "cancel"

    # -------------------------
    # Determine target (Hybrid Targeting)
    # -------------------------
    target_mode = skill["target"]
    target = None

    if target_mode == "enemy":
        target = prompt_player_for_enemy_target(enemies)
        if target is None:
            print("No valid targets! Skill canceled.")
            return "cancel"

    elif target_mode == "self":
        target = user

    elif target_mode == "ally":
        target = auto_target_lowest_hp(allies or [user])
        if target is None:
            print("No valid allies! Skill canceled.")
            return "cancel"

    # AoE and all-allies require no manual target selection

    # -------------------------
    # Deduct resources
    # -------------------------
    user.current_mp -= cost_mp
    user.current_sp -= cost_sp

    # Assign cooldown
    user.skill_cooldowns[skill_id] = skill["cooldown"]

    # -------------------------
    # Route by skill type
    # -------------------------
    stype = skill["type"]

    if stype in ["damage", "multi_hit", "aoe", "ultimate", "dot"]:
        apply_damage_skill(user, skill, target, enemies)

    if stype == "heal":
        apply_healing_skill(user, skill, target, allies or [user])

    if skill.get("status_effects"):
        apply_status_effects(user, skill, target, enemies, allies or [user])

    print(f"{user.name} used {skill['name']}!")
    return "ok"


# ============================================================
# DAMAGE HANDLING
# ============================================================

def apply_damage_skill(user, skill, target, enemies):
    stype = skill["type"]
    dmg_block = skill.get("damage")

    # AoE / Ultimate
    if stype in ["aoe", "ultimate"] and skill["target"] == "all_enemies":
        for enemy in enemies:
            if enemy and not enemy.is_dead():
                _apply_single_hit(user, enemy, skill)
        return

    # Pure DoT → no immediate damage
    if stype == "dot":
        return

    # Single-target / multi-hit
    if target is None or target.is_dead():
        return

    hits = dmg_block.get("hits", 1) if dmg_block else 1
    for _ in range(hits):
        _apply_single_hit(user, target, skill)


def _apply_single_hit(user, target, skill):
    damage, is_crit, dodged = calculate_damage(user, target, skill)

    if dodged:
        print(f"{user.name}'s {skill['name']} missed {target.name}!")
        return

    crit_text = " (CRIT!)" if is_crit else ""
    target.take_damage(user, damage, source=skill["name"] + crit_text)


# ============================================================
# HEALING
# ============================================================

def apply_healing_skill(user, skill, target, allies):
    heal_block = skill.get("healing")
    if not heal_block:
        return

    # Determine target if needed
    if skill["target"] == "ally":
        target = auto_target_lowest_hp(allies)

    if target is None or target.is_dead():
        print("No valid healing target!")
        return

    base = heal_block.get("flat", 0)
    scaling = heal_block.get("scaling", {})

    for stat_name, coeff in scaling.items():
        if hasattr(user, "get_scaled_stat"):
            final_attr = user.get_scaled_stat(stat_name)
        else:
            final_attr = getattr(user, stat_name.lower(), 0)
        base += final_attr * coeff

    # Variance
    import random
    base *= random.uniform(0.9, 1.1)

    amount = max(1, int(base))
    before = target.current_hp
    target.current_hp = min(target.max_hp, target.current_hp + amount)

    print(f"{user.name} heals {target.name} for {amount} HP! ({before} → {target.current_hp})")


# ============================================================
# STATUS EFFECTS
# ============================================================

def apply_status_effects(user, skill, target, enemies, allies):
    effects = skill.get("status_effects", [])
    if not effects:
        return

    stype = skill["type"]
    target_mode = skill["target"]

    # AoE statuses
    if stype in ["aoe", "ultimate"] and target_mode == "all_enemies":
        for enemy in enemies:
            if enemy and not enemy.is_dead():
                for eff in effects:
                    _apply_single_status(user, enemy, eff)
        return

    # Single-target
    if target is None or target.is_dead():
        return

    for eff in effects:
        _apply_single_status(user, target, eff)


def _apply_single_status(user, target, eff):
    name = eff["name"]
    duration = eff.get("duration", 1)

    # Copy nested data dict if present
    data = dict(eff.get("data", {}))

    # Also support legacy top-level keys
    for key in ["amount_per_turn", "flat", "percent", "stacking"]:
        if key in eff:
            data[key] = eff[key]


    # Attach applier for DoT attribution
    data["applier"] = user

    definition = STATUS_DEFINITIONS.get(name)
    effect_type = definition["type"] if definition else "debuff"

    target.apply_status(name, effect_type, duration, data)
    print(f"{target.name} is affected by {name} ({duration} turns).")
