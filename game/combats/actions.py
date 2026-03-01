from game.combats.damage import calculate_damage
from game.status.status_definitions import STATUS_DEFINITIONS
import random


def player_attack(player, enemy, action=None):

    # ============================================================
    # Helper: unified status application
    # ============================================================
    def apply_status_effects(effect_list, hit_landed=True):
        if not effect_list:
            return

        for se in effect_list:
            definition = STATUS_DEFINITIONS[se["name"]]

            # Respect chance
            effect_chance = se.get("chance", definition.get("chance", 1.0))
            if random.random() > effect_chance:
                continue

            # If this is a damage-based action and the hit missed, skip
            if not hit_landed and action and action.get("damage"):
                continue

            # Determine target
            target = enemy  # default for player actions

            if se.get("target") == "self":
                target = player

            elif se.get("target") == "ally" and hasattr(player, "party"):
                allies = [a for a in player.party if not a.is_dead() and a is not player]
                if allies:
                    target = min(allies, key=lambda a: a.current_hp / a.max_hp)

            # Apply status
            target.apply_status(
                name=se["name"],
                effect_type=definition["type"],
                duration=se["duration"],
                data=se.get("data", {})
            )

    # ============================================================
    # 1. BASIC ATTACK (no action passed)
    # ============================================================
    if action is None:
        print(f"[DEBUG] Player hit_chance={player.hit_chance:.3f}, Enemy dodge={enemy.dodge_chance:.3f}")
        dmg, is_crit, dodged = calculate_damage(player, enemy)

        if dodged:
            print(">>> DODGED!!!")
            return

        if is_crit:
            print(">>> CRITICAL HIT!")

        enemy.take_damage(dmg)
        print(f"{player.name} attacks {enemy.name} for {dmg} damage!")
        return

    # ============================================================
    # 2. NON-DAMAGE SKILLS
    # ============================================================
    if action.get("skip") or "damage" not in action:
        print(f"[DEBUG] {player.name} uses {action['name']} (non-damage action)")
        apply_status_effects(action.get("status_effects", []), hit_landed=True)
        return

    # ============================================================
    # 3. DAMAGE SKILLS
    # ============================================================
    print(f"[DEBUG] Player hit_chance={player.hit_chance:.3f}, Enemy dodge={enemy.dodge_chance:.3f}")
    print(f"[DEBUG] Action chosen: {action['name']}")

    damage_block = action["damage"]
    hits = damage_block.get("hits", 1)
    hit_landed = False

    for hit_index in range(hits):
        dmg, is_crit, dodged = calculate_damage(player, enemy, action)

        if dodged:
            print(f"{enemy.name} dodged hit {hit_index+1}!")
            continue

        if is_crit:
            print(f"Hit {hit_index+1}: CRITICAL HIT!")

        hit_landed = True
        enemy.take_damage(dmg)
        print(f"Hit {hit_index+1}: {action['name']} | {player.name} deals {dmg} damage!")

    # ============================================================
    # 4. Apply status effects (unified)
    # ============================================================
    apply_status_effects(action.get("status_effects", []), hit_landed=hit_landed)


def enemy_use_action(enemy, player, action):

    # ============================================================
    # Helper: Apply status effects with unified targeting
    # ============================================================
    def apply_status_effects(effect_list, hit_landed=True):
        if not effect_list:
            return

        for se in effect_list:
            definition = STATUS_DEFINITIONS[se["name"]]

            # Respect chance
            effect_chance = se.get("chance", definition.get("chance", 1.0))
            if random.random() > effect_chance:
                continue

            # If this is a damage-based action and the hit missed, skip
            if not hit_landed and action.get("damage"):
                continue

            # Determine target
            target = player  # default

            if se.get("target") == "self":
                target = enemy

            elif se.get("target") == "ally" and hasattr(enemy, "current_wave_enemies"):
                allies = [a for a in enemy.current_wave_enemies if not a.is_dead() and a is not enemy]
                if allies:
                    target = min(allies, key=lambda a: a.current_hp / a.max_hp)

            # Apply status
            target.apply_status(
                name=se["name"],
                effect_type=definition["type"],
                duration=se["duration"],
                data=se.get("data", {})
            )

            # Special stun logic
            if "stun_chance" in definition and target is player:
                if random.random() < definition["stun_chance"]:
                    player.apply_status("Stun", "stun", 1, {})
                    print(f"{player.name} is jolted by lightning and STUNNED!")

    # ============================================================
    # 1. NON-DAMAGE ACTIONS (buffs, curses, rituals)
    # ============================================================
    if action.get("skip") or "damage" not in action:
        print(f"[AI DEBUG] {enemy.name} uses {action['name']} (non-damage action)")
        apply_status_effects(action.get("status_effects", []), hit_landed=True)
        return

    # ============================================================
    # 2. DAMAGE ACTIONS
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

    # ============================================================
    # 3. Apply status effects (unified)
    # ============================================================
    apply_status_effects(action.get("status_effects", []), hit_landed=hit_landed)

    # ============================================================
    # 4. Apply HoT effects
    # ============================================================
    if "hot_effects" in action:
        for hot in action["hot_effects"]:
            definition = STATUS_DEFINITIONS[hot["name"]]

            target = player
            if hot.get("target") == "self":
                target = enemy
            elif hot.get("target") == "ally" and hasattr(enemy, "current_wave_enemies"):
                allies = [a for a in enemy.current_wave_enemies if not a.is_dead() and a is not enemy]
                if allies:
                    target = min(allies, key=lambda a: a.current_hp / a.max_hp)

            target.apply_status(
                name=hot["name"],
                effect_type=definition["type"],
                duration=hot["duration"],
                data={"amount_per_turn": hot.get("amount_per_turn", 0)}
            )
            print(f"{enemy.name} applies {hot['name']} to {target.name}!")

    # ============================================================
    # 5. Custom effects (Spirit Drain)
    # ============================================================
    if "custom_effects" in action:
        for ce in action["custom_effects"]:
            if ce["type"] == "drain_resources":
                player.current_sp = max(0, player.current_sp - ce["sp_amount"])
                player.current_mp = max(0, player.current_mp - ce["mp_amount"])
                print(f"{player.name} loses {ce['sp_amount']} Stamina and {ce['mp_amount']} Mana!")

                enemy.current_sp = min(enemy.max_sp, enemy.current_sp + ce["self_sp_restore"])
                enemy.current_mp = min(enemy.max_mp, enemy.current_mp + ce["self_mp_restore"])
                print(f"{enemy.name} restores {ce['self_sp_restore']} SP and {ce['self_mp_restore']} MP!")