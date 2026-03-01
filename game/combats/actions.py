from game.combats.damage import calculate_damage
from game.status.status_definitions import STATUS_DEFINITIONS

def player_attack(player, enemy):
    print(f"[DEBUG] Player hit_chance={player.hit_chance:.3f}, Enemy dodge={enemy.dodge_chance:.3f}")

    damage, is_crit, dodged = calculate_damage(player, enemy)
    
    if dodged:
        print(">>> DODGED!!!")
        return

    if is_crit:
        print(">>> CRITICAL HIT!")

    enemy.take_damage(damage)
    print(f"{player.name} attacks {enemy.name} for {damage} damage!")



def enemy_use_action(enemy, player, action):

    # ============================================================
    # 1. HEALING ACTIONS (Goblin Shaman, future healers)
    # ============================================================
    if "heal_target" in action:
        target = action["heal_target"]

        heal_percent = enemy.heal_ability.get("heal_percent", 0)
        heal_amount = int(target.max_hp * heal_percent)

        before = target.current_hp
        target.current_hp = min(target.max_hp, target.current_hp + heal_amount)
        healed = target.current_hp - before

        print(f"{enemy.name} casts Mend Flesh on {target.name}, healing {healed} HP!")
        return

    # ============================================================
    # 2. NON-DAMAGE ACTIONS (buffs, telegraphs, skip)
    # ============================================================
    if action.get("skip") or "damage" not in action:
        print(f"[AI DEBUG] {enemy.name} uses {action['name']} (non-damage action)")

        if "status_effects" in action:
            for se in action["status_effects"]:
                definition = STATUS_DEFINITIONS[se["name"]]

                import random
                effect_chance = se.get("chance", definition.get("chance", 1.0))
                if random.random() > effect_chance:
                    continue

                player.apply_status(
                    name=se["name"],
                    effect_type=definition["type"],
                    duration=se["duration"],
                    data=se.get("data", {})
                )
        return

    # ============================================================
    # 3. DAMAGE ACTIONS (unchanged)
    # ============================================================
    print(f"[DEBUG] {enemy.name} hit_chance={enemy.hit_chance:.3f}, {player.name} dodge={player.dodge_chance:.3f}")
    print(f"[AI DEBUG] Action chosen: {action['name']}")

    damage_block = action["damage"]
    hits = damage_block.get("hits", 1)
    second_hit_acc = action.get("second_hit_accuracy")

    hit_landed = False

    for hit_index in range(hits):
        original_hit = enemy.hit_chance

        if hit_index == 1 and second_hit_acc is not None:
            enemy.hit_chance = second_hit_acc

        dmg, is_crit, dodged = calculate_damage(enemy, player, action)
        enemy.hit_chance = original_hit

        if dodged:
            print(f"{player.name} dodged hit {hit_index+1}!")
            continue

        if is_crit:
            print(f"Hit {hit_index+1}: CRITICAL HIT!")

        hit_landed = True
        player.take_damage(enemy, dmg)
        print(f"Hit {hit_index+1}: {action['name']} | {enemy.name} deals {dmg} damage!")

    if hit_landed and "status_effects" in action:
        for se in action["status_effects"]:
            definition = STATUS_DEFINITIONS[se["name"]]

            import random
            effect_chance = se.get("chance", definition.get("chance", 1.0))
            if random.random() > effect_chance:
                continue

            # Determine target
            target = player
            if se.get("target") == "self":
                target = enemy
            elif se.get("target") == "ally" and hasattr(enemy, "current_wave_enemies"):
                allies = [a for a in enemy.current_wave_enemies if not a.is_dead()]
                if allies:
                    target = min(allies, key=lambda a: a.current_hp / a.max_hp)

            # Apply status
            target.apply_status(
                name=se["name"],
                effect_type=definition["type"],
                duration=se["duration"],
                data=se.get("data", {})
            )

            if "stun_chance" in definition:
                if random.random() < definition["stun_chance"]:
                    player.apply_status("Stun", "stun", 1, {})
                    print(f"{player.name} is jolted by lightning and STUNNED!")

            # --- APPLY HOT (Heal Over Time) ---
    if "hot_effects" in action:
        for hot in action["hot_effects"]:
            definition = STATUS_DEFINITIONS[hot["name"]]
            target = player
            if hot.get("target") == "self":
                target = enemy
            elif hot.get("target") == "ally" and hasattr(enemy, "current_wave_enemies"):
                allies = [a for a in enemy.current_wave_enemies if not a.is_dead()]
                if allies:
                    target = min(allies, key=lambda a: a.current_hp / a.max_hp)
            target.apply_status(
                name=hot["name"],
                effect_type=definition["type"],
                duration=hot["duration"],
                data={"amount_per_turn": hot.get("amount_per_turn", 0)}
            )
            print(f"{enemy.name} applies {hot['name']} to {target.name}!")