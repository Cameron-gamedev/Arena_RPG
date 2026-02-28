from game.status.status_definitions import STATUS_DEFINITIONS

def use_item(player, inventory):
    print("\nChoose an item:")

    indexed_slots = []

    for i, slot in enumerate(inventory.slots):
        if slot is None:
            continue
        indexed_slots.append((i, slot))
        print(f" {len(indexed_slots)}. {slot.name} x{slot.quantity}")

    print(" b. Back")

    if not indexed_slots:
        print("You have no items.")
        return False
    
    while True:
        choice = input("Item number: ").strip()

        if choice.lower() == "b":
            return False
        
        if not choice.isdigit():
            print("Invalid choice.")
            continue

        idx = int(choice) - 1
        if idx < 0 or idx >= len(indexed_slots):
            print("Invalid choice.")
            continue

        slot_index, item = indexed_slots[idx]

        return apply_item_effect(player, inventory, slot_index, item)


def apply_item_effect(player, inventory, slot_index, item):
    if item.effect is None:
        print("This item has no effect.")
        return False
    
    effect = item.effect
    kind = effect.get("kind")

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
            player.current_mp = min(player.max_max, player.current_mp + amount)
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
    
    elif kind == "restore_over_time":
        target = effect.get("target")
        percent = effect.get("percent", 0)
        duration = effect.get("duration", 1)

        if target == "hp":
            max_val = player.max_hp
        elif target == "mp":
            max_val = player.max_mp
        elif target == "sp":
            max_val = player.max_sp
        else:
            print("Unknown regen target.")
            return False
        
        total_amount = int(max_val * percent)
        amount_per_turn = max(1, total_amount // duration)

        if target == "hp":
            status_name = "RegenHP"
        elif target == "mp":
            status_name = "RegenMP"
        elif target == "sp":
            status_name = "RegenSP"

        player.apply_status(
            name=status_name,
            effect_type="hot",
            duration=duration,
            data={"amount_per_turn": amount_per_turn}
        )
 
        print(f"{item.name} will restore {total_amount} {target.upper()} over {duration} turns!")

    elif kind == "buff":
        stat = effect.get("stat")
        flat = effect.get("flat", 0)
        percent = effect.get("percent", 0)
        duration = effect.get("duration", 1)

        status_name = f"Buff{stat.capitalize()}"
        player.apply_status(
            name=status_name,
            effect_type="buff",
            duration=duration,
            data={"flat": flat, "percent": percent}
        )        
        
        print(f"{item.name} increases {stat} for {duration} turns!")

    elif kind == "status":
        status_name = effect.get("status_name")
        duration = effect.get("duration", 1)
        amount_per_turn = effect.get("amount_per_turn", 0)

        player.apply_status(
            name=status_name,
            effect_type=STATUS_DEFINITIONS[status_name]["type"],
            duration=duration,
            data={"amount_per_turn": amount_per_turn}
        )

        print(f"{item.name} inflicts {status_name} for {duration} turns!")

    else:
        print("This type of effect is not implemented yet.")
        return False
    
    item.quantity -= 1
    if item.quantity <= 0:
        inventory.slots[slot_index] = None

    return True
