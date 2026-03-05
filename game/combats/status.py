from game.status.status_definitions import STATUS_DEFINITIONS
from game.combats.healing import apply_heal


def process_status_effects(target):
    """
    Handles DOT, HOT, and duration ticking for all status effects.
    Removes expired effects and recalculates stats when needed.
    """

    if not hasattr(target, "status_effects") or not target.status_effects:
        return
    if target.is_dead():
        return

    expired = []

    for effect in target.status_effects:
        name = effect["name"]
        definition = STATUS_DEFINITIONS.get(name)
        if not definition:
            continue

        effect_type = definition["type"]
        data = effect.get("data", {})

        # -----------------------------
        # HEAL OVER TIME (HOT)
        # -----------------------------
        if effect_type == "hot":
            resource = definition["target"]
            amount = data.get("amount_per_turn", 0)

            apply_heal(target, amount, resource=resource, source=name)

            if resource == "mp":
                before = target.current_mp
                target.current_mp = min(target.max_mp, target.current_mp + amount)
                restored = target.current_mp - before
                print(f"{target.name} regenerates {restored} MP from {name}.")

            elif resource == "sp":
                before = target.current_sp
                target.current_sp = min(target.max_sp, target.current_sp + amount)
                restored = target.current_sp - before
                print(f"{target.name} regenerates {restored} SP from {name}.")

        # -----------------------------
        # DAMAGE OVER TIME (DOT)
        # -----------------------------
        elif effect_type == "dot":
            amount = data.get("amount_per_turn", 0)
            applier = data.get("applier")

            attacker_obj = applier if hasattr(applier, "name") else None
            target.take_damage(attacker=attacker_obj, amount=amount, source=name)

        # -----------------------------
        # TICK DURATION
        # -----------------------------
        effect["duration"] -= 1
        if effect["duration"] <= 0:
            expired.append(effect)

    # -----------------------------
    # REMOVE EXPIRED EFFECTS
    # -----------------------------
    for e in expired:
        target.status_effects.remove(e)

    # -----------------------------
    # RECALCULATE STATS IF ANY BUFF/DEBUFF EXPIRED
    # -----------------------------
    if expired:
        target.recalculate_stats()


def process_regen_effects(player):
    """
    Handles the separate regen system (active_regen_effects).
    This is distinct from HOT effects and is used for skills that apply regen.
    """

    if not player.active_regen_effects or player.is_dead():
        return

    print("\n-- Regen Effects --")
    expired = []

    for effect in player.active_regen_effects:
        amount = effect["amount_per_turn"]
        target = effect["target"]

        if target == "hp":
            before = player.current_hp
            player.current_hp = min(player.max_hp, player.current_hp + amount)
            healed = player.current_hp - before
            print(f"{player.name} regenerates {healed} HP from ongoing effects.")

        elif target == "mp":
            before = player.current_mp
            player.current_mp = min(player.max_mp, player.current_mp + amount)
            restored = player.current_mp - before
            print(f"{player.name} regenerates {restored} MP from ongoing effects.")

        elif target == "sp":
            before = player.current_sp
            player.current_sp = min(player.max_sp, player.current_sp + amount)
            restored = player.current_sp - before
            print(f"{player.name} regenerates {restored} SP from ongoing effects.")

        effect["turns_left"] -= 1
        if effect["turns_left"] <= 0:
            expired.append(effect)

    for e in expired:
        player.active_regen_effects.remove(e)


def list_status_effects(target):
    """
    Returns a simple string summary of active status effects.
    """
    if not target.status_effects:
        return "None"

    parts = []
    for effect in target.status_effects:
        name = effect["name"]
        duration = effect["duration"]
        parts.append(f"{name} ({duration})")

    return ", ".join(parts)


def apply_passive_regen(target):
    """
    Applies passive regen (HP/MP/SP) from class identity or equipment.
    """

    # HP regen
    if target.passive_hp_regen > 0 and not target.is_dead():
        before = target.current_hp
        target.current_hp = min(target.max_hp, target.current_hp + target.passive_hp_regen)
        healed = target.current_hp - before
        if healed > 0:
            print(f"{target.name} passively regenerates {healed} HP.")

    # MP regen
    if target.passive_mp_regen > 0:
        before = target.current_mp
        target.current_mp = min(target.max_mp, target.current_mp + target.passive_mp_regen)
        restored = target.current_mp - before
        if restored > 0:
            print(f"{target.name} regenerates {restored} MP.")

    # SP regen
    if target.passive_sp_regen > 0:
        before = target.current_sp
        target.current_sp = min(target.max_sp, target.current_sp + target.passive_sp_regen)
        restored = target.current_sp - before
        if restored > 0:
            print(f"{target.name} regenerates {restored} SP.")


def get_regen_summary(player):
    """
    Returns a dict summarizing total regen per turn from active_regen_effects.
    """
    summary = {"hp": 0, "mp": 0, "sp": 0}

    for effect in player.active_regen_effects:
        summary[effect["target"]] += effect["amount_per_turn"]

    return summary
