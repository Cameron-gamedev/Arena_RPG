from game.status.status_definitions import STATUS_DEFINITIONS


def use_item(player, inventory, index):
    # Validate index
    if index < 0 or index >= len(inventory.slots):
        print("Invalid item selection.")
        return False

    item = inventory.slots[index]
    if item is None:
        print("No item in that slot.")
        return False

    # Apply the effect
    result = apply_item_effect(player, inventory, index, item)
    return result


def apply_item_effect(player, inventory, slot_index, item):
    if item.effect is None:
        print("This item has no effect.")
        return False

    effect = item.effect
    kind = effect.get("kind")

    # ------------------------------------------------------------
    # INSTANT RESTORE (HP/MP/SP)
    # ------------------------------------------------------------
    if kind == "restore_instant":
        target = effect.get("target")
        percent = effect.get("percent", 0)
        flat = effect.get("flat", 0)

        if target == "hp":
            max_val = player.max_hp
            before = player.current_hp
            amount = int(max_val * percent) + flat
            player.current_hp = min(player.max_hp, player.current_hp + amount)
            healed = player.current_hp - before
            print(f"{item.name} restores {healed} HP!")

        elif target == "mp":
            max_val = player.max_mp
            before = player.current_mp
            amount = int(max_val * percent) + flat
            player.current_mp = min(player.max_mp, player.current_mp + amount)
            restored = player.current_mp - before
            print(f"{item.name} restores {restored} MP!")

        elif target == "sp":
            max_val = player.max_sp
            before = player.current_sp
            amount = int(max_val * percent) + flat
            player.current_sp = min(player.max_sp, player.current_sp + amount)
            restored = player.current_sp - before
            print(f"{item.name} restores {restored} Stamina!")

        else:
            print("Unknown restore target.")
            return False

    # ------------------------------------------------------------
    # RESTORE OVER TIME (RegenHP / RegenMP / RegenSP)
    # ------------------------------------------------------------
    elif kind == "restore_over_time":
        target = effect.get("target")
        percent = effect.get("percent", 0)
        duration = effect.get("duration", 1)

        if target == "hp":
            max_val = player.max_hp
            status_name = "RegenHP"
        elif target == "mp":
            max_val = player.max_mp
            status_name = "RegenMP"
        elif target == "sp":
            max_val = player.max_sp
            status_name = "RegenSP"
        else:
            print("Unknown regen target.")
            return False

        total_amount = int(max_val * percent)
        amount_per_turn = max(1, total_amount // duration)

        player.apply_status(
            name=status_name,
            effect_type="hot",
            duration=duration,
            data={"amount_per_turn": amount_per_turn}
        )

        print(f"{item.name} will restore {total_amount} {target.upper()} over {duration} turns!")


    # ------------------------------------------------------------
    # APPLY A STATUS EFFECT (poison, bleed, etc.)
    # ------------------------------------------------------------
    elif kind == "status":
        status_name = effect.get("status_name")
        duration = effect.get("duration", 1)

        # NEW: pull full data dict (flat, percent, amount_per_turn, stacking, etc.)
        data = effect.get("data", {})

        player.apply_status(
            name=status_name,
            effect_type=STATUS_DEFINITIONS[status_name]["type"],
            duration=duration,
            data=data
        )

        print(f"{item.name} applies {status_name} for {duration} turns!")


    else:
        print("This type of effect is not implemented yet.")
        return False

    # ------------------------------------------------------------
    # CONSUME ITEM (stackable or single)
    # ------------------------------------------------------------
    item.quantity -= 1
    if item.quantity <= 0:
        inventory.slots[slot_index] = None

    return True
