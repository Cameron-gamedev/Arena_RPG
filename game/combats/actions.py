from game.combats.damage import calculate_damage
from game.status.status_definitions import STATUS_DEFINITIONS
from game.status.apply_status_effects import apply_status_effects

import random

# ============================================================
# PLAYER BASIC ATTACK ONLY
# ============================================================
def player_attack(player, enemy):
    print(f"[DEBUG] Player hit_chance={player.hit_chance:.3f}, Enemy dodge={enemy.dodge_chance:.3f}")
    print("=" * 50)

    damage, is_crit, dodged = calculate_damage(player, enemy, skill=None)

    if dodged:
        print(">>> DODGED!!!")
        return

    if is_crit:
        print(">>> CRITICAL HIT!")

    enemy.take_damage(player, damage, source="Basic Attack")


# ============================================================
# ENEMY ACTION SYSTEM (FULLY UNIFIED)
# ============================================================
def enemy_use_action(enemy, player, action):

    # Always define hit_landed so it exists for all branches
    hit_landed = False

    # ------------------------------------------------------------
    # 1. NON-DAMAGE ACTIONS (buffs, curses, rituals)
    # ------------------------------------------------------------
    if action.get("skip") or "damage" not in action:
        print(f"[AI DEBUG] {enemy.name} uses {action['name']} (non-damage action)")
        print("="*50)

        apply_status_effects(
            source=enemy,
            target_group={
                "default": player,
                "player": player,
                "self": enemy,
                "enemies": getattr(enemy, "current_wave_enemies", []),
                "allies": getattr(enemy, "current_wave_enemies", [])
            },
            effect_list=action.get("status_effects", []),
            hit_landed=True
        )
        return

    # ------------------------------------------------------------
    # 2. DAMAGE ACTIONS
    # ------------------------------------------------------------
    print(f"[DEBUG] {enemy.name} hit_chance={enemy.hit_chance:.3f}, {player.name} dodge={player.dodge_chance:.3f}")
    print("="*50)
    print(f"[AI DEBUG] Action chosen: {action['name']}")
    print("="*50)
    
    damage_block = action["damage"]
    hits = damage_block.get("hits", 1)

    # Multi-hit accuracy support
    second_hit_acc = action.get("second_hit_accuracy")
    third_hit_acc = action.get("third_hit_accuracy")

    for hit_index in range(hits):
        original_hit = enemy.hit_chance

        # Support for 2nd and 3rd hit accuracy overrides
        if hit_index == 1 and second_hit_acc is not None:
            enemy.hit_chance = second_hit_acc
        elif hit_index == 2 and third_hit_acc is not None:
            enemy.hit_chance = third_hit_acc

        dmg, is_crit, dodged = calculate_damage(enemy, player, action)
        enemy.hit_chance = original_hit

        if dodged:
            print(f"{player.name} dodged hit {hit_index+1}!")
            continue

        if is_crit:
            print(f"Hit {hit_index+1}: CRITICAL HIT!")

        hit_landed = True
        player.take_damage(enemy, dmg, source=action["name"])
        print(f"Hit {hit_index+1}: {action['name']} | {enemy.name} deals {dmg} damage!")

    # ------------------------------------------------------------
    # 3. Apply status effects (unified)
    # ------------------------------------------------------------
    apply_status_effects(
        source=enemy,
        target_group={
            "default": player,
            "player": player,
            "self": enemy,
            "enemies": getattr(enemy, "current_wave_enemies", []),
            "allies": getattr(enemy, "current_wave_enemies", [])
        },
        effect_list=action.get("status_effects", []),
        hit_landed=hit_landed
    )

    # ------------------------------------------------------------
    # 4. Apply HoT effects (unified)
    # ------------------------------------------------------------
    if "hot_effects" in action:
        for hot in action["hot_effects"]:
            definition = STATUS_DEFINITIONS[hot["name"]]

            # Determine target
            target = player
            if hot.get("target") == "self":
                target = enemy
            elif hot.get("target") == "ally":
                allies = getattr(enemy, "current_wave_enemies", [])
                allies = [a for a in allies if not a.is_dead() and a is not enemy]
                if allies:
                    target = min(allies, key=lambda a: a.current_hp / a.max_hp)

            target.apply_status(
                name=hot["name"],
                effect_type=definition["type"],
                duration=hot["duration"],
                data={"amount_per_turn": hot.get("amount_per_turn", 0)}
            )
            print(f"{enemy.name} applies {hot['name']} to {target.name}!")

    # ------------------------------------------------------------
    # 5. Custom effects (Spirit Drain)
    # ------------------------------------------------------------
    if "custom_effects" in action:
        for ce in action["custom_effects"]:
            if ce["type"] == "drain_resources":
                player.current_sp = max(0, player.current_sp - ce["sp_amount"])
                player.current_mp = max(0, player.current_mp - ce["mp_amount"])
                print(f"{player.name} loses {ce['sp_amount']} Stamina and {ce['mp_amount']} Mana!")

                enemy.current_sp = min(enemy.max_sp, enemy.current_sp + ce["self_sp_restore"])
                enemy.current_mp = min(enemy.max_mp, enemy.current_mp + ce["self_mp_restore"])
                print(f"{enemy.name} restores {ce['self_sp_restore']} SP and {ce['self_mp_restore']} MP!")
