from game.status.status_definitions import STATUS_DEFINITIONS

def process_status_effects(target):
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
        data = effect["data"]

        # HOT
        if effect_type == "hot":
            resource = definition["target"]
            amount = data.get("amount_per_turn", 0)

            if resource == "hp":
                before = target.current_hp
                target.current_hp = min(target.max_hp, target.current_hp + amount)
                healed = target.current_hp - before
                print(f"{target.name} regenerates {healed} HP from {name}.")
            elif resource == "mp":
                before = target.current_mp
                target.current_mp = min(target.max_mp, target.current_mp + amount)
                restored = target.current_mp - before
                print(f"{target.name} regenerates {restored} MP from {name}.")
            elif resource == "sp":
                before = target.current_sp
                target.current_sp = min(target.max_sp, target.current_sp + amount)
                restored = target.current_sp - before
                print(f"{target.name} regenerates {restored} SP from {name}.")

        # DOT
        elif effect_type == "dot":
            resource = definition["target"]
            amount = data.get("amount_per_turn", 0)

            if resource == "hp":
                before = target.current_hp
                target.current_hp = max(0, target.current_hp - amount)
                dmg = before - target.current_hp
                print(f"{target.name} takes {dmg} damage from {name}!")

        effect["duration"] -= 1
        if effect["duration"] <= 0:
            expired.append(effect)

    for e in expired:
        target.status_effects.remove(e)


def process_regen_effects(player):
    if not player.active_regen_effects:
        return
    if player.is_dead():
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


def process_buffs(player):
    if not player.active_buffs:
        return

    expired = []
    for buff in player.active_buffs:
        buff["turns_left"] -= 1
        if buff["turns_left"] <= 0:
            expired.append(buff)

    for b in expired:
        player.active_buffs.remove(b)

    if expired:
        player.recalculate_stats()
        print("\n-- Buffs Expired --")
        for b in expired:
            print(f"{b['stat']} buff has worn off.")


def list_status_effects(target):
    if not target.status_effects:
        return "None"
    parts = []
    for effect in target.status_effects:
        name = effect["name"]
        duration = effect["duration"]
        parts.append(f"{name} ({duration})")
    return ", ".join(parts)


def apply_passive_regen(target):
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
    summary = {"hp": 0, "mp": 0, "sp": 0}
    for effect in player.active_regen_effects:
        summary[effect["target"]] += effect["amount_per_turn"]
    return summary
