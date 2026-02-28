from game.combats.damage import calculate_damage
from game.status.status_definitions import STATUS_DEFINITIONS

def player_choose_skill(player):
    from game.skills.skills import SKILLS_DB

    if not hasattr(player, "skills") or len(player.skills) == 0:
        print("You have no skills.")
        return None
    
    print("\nChoose a skill:")
    for i, skill_id in enumerate(player.skills, start=1):
        skill = SKILLS_DB[skill_id]
        remaining = player.skill_cooldowns.get(skill_id, 0)
        cd_text = f"(Cooldown: {remaining})" if remaining > 0 else "Ready"
        print(f" {i}. {skill['name']} - {skill['description']} | {cd_text}")

    print("b. Back")

    while True:
        choice = input("Skill number: ").strip()

        if choice.lower() == "b":
            return None
        
        if not choice.isdigit():
            print("Invalid choice.")
            continue

        idx = int(choice) - 1
        if 0 <= idx < len(player.skills):
            return player.skills[idx]

        print("Invalid choice.")


def choose_single_target(player, skill, enemies):
    living = [e for e in enemies if not e.is_dead()]
    if not living:
        print("No valid targets.")
        return

    print("Choose a target:")
    for i, e in enumerate(living, start=1):
        print(f"{i}. {e.name} {e.current_hp}/{e.max_hp} HP")

    choice = input("Target number: ").strip()
    if not choice.isdigit():
        print("Invalid choice.")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(living):
        print("Invalid choice.")
        return

    target = living[idx]

    hit_landed = False
    hits = skill["damage"].get("hits", 1)

    for i in range(hits):
        dmg, is_crit, dodged = calculate_damage(player, target, skill)

        if dodged:
            print(f"Hit {i+1}: {target.name} dodged the attack!")
            continue

        if is_crit:
            print(f"Hit {i+1}: >> CRITICAL HIT!")

        hit_landed = True
        target.take_damage(dmg)
        print(f"Hit {i+1}: {skill['name']} deals {dmg} damage to {target.name}!")

    if hit_landed and "status_effects" in skill:
        for se in skill["status_effects"]:
            target.apply_status(
                name=se["name"],
                effect_type=STATUS_DEFINITIONS[se["name"]]["type"],
                duration=se["duration"],
                data={"amount_per_turn": se.get("amount_per_turn", 0)}
            )


def choose_multi_targets(player, skill, enemies):
    living = [e for e in enemies if not e.is_dead()]
    if not living:
        print("No valid targets")
        return

    print("The skill strikes at All enemies!")

    hits = skill["damage"].get("hits", 1)

    for enemy in living:
        print(f"\n{enemy.name}:")
        enemy_hit = False

        for i in range(hits):
            dmg, is_crit, dodged = calculate_damage(player, enemy, skill)

            if dodged:
                print(f"  Hit {i+1}: dodged!")
                continue

            if is_crit:
                print(f"  Hit {i+1}: >>> CRITICAL HIT!")

            enemy_hit = True
            enemy.take_damage(dmg)
            print(f"  Hit {i+1}: {dmg} damage!")

        if enemy_hit and "status_effects" in skill:
            for se in skill["status_effects"]:
                enemy.apply_status(
                    name=se["name"],
                    effect_type=STATUS_DEFINITIONS[se["name"]]["type"],
                    duration=se["duration"],
                    data={"amount_per_turn": se.get("amount_per_turn", 0)}
                )


def can_use_skill(player, skill_id, skill):
    remaining = player.skill_cooldowns.get(skill_id, 0)
    if remaining > 0:
        return False, f"{skill['name']} is on cooldown for {remaining} more turn(s)!"

    cost_type = skill.get("cost_type")
    cost = skill.get("cost", 0)

    if cost_type == "mp":
        if player.current_mp < cost:
            return False, "Not enough MP!"
        return True, None

    elif cost_type == "sp":
        if player.current_sp < cost:
            return False, "Not enough Stamina!"
        return True, None

    return True, None


def use_skill(player, skill_id, enemies):
    from game.skills.skills import SKILLS_DB
    skill = SKILLS_DB[skill_id]

    can_use, message = can_use_skill(player, skill_id, skill)
    if not can_use:
        print(message)
        return False

    cost_type = skill.get("cost_type")
    cost = skill.get("cost", 0)

    if cost_type == "mp":
        player.current_mp -= cost
    elif cost_type == "sp":
        player.current_sp -= cost

    print(f"\n{player.name} uses {skill['name']}!")

    if skill["target"] == "enemy":
        choose_single_target(player, skill, enemies)
    elif skill["target"] == "all_enemies":
        choose_multi_targets(player, skill, enemies)

    cd = skill.get("cooldown", 0)
    if cd > 0:
        player.skill_cooldowns[skill_id] = cd

    return True

