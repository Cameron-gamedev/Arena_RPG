def apply_heal(target, amount, resource="hp", source=None):
    amount = max(0, int(amount))

    if resource == "hp":
        before = target.current_hp
        target.current_hp = min(target.max_hp, target.current_hp + amount)
        healed = target.current_hp - before
        print(f"{target.name} recovers {healed} HP from {source or 'healing'}.")

    elif resource == "mp":
        before = target.current_mp
        target.current_mp = min(target.max_mp, target.current_mp + amount)
        restored = target.current_mp - before
        print(f"{target.name} recovers {restored} MP from {source or 'healing'}.")

    elif resource == "sp":
        before = target.current_sp
        target.current_sp = min(target.max_sp, target.current_sp + amount)
        restored = target.current_sp - before
        print(f"{target.name} recovers {restored} SP from {source or 'healing'}.")