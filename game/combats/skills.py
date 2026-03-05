def player_choose_skill(player):
    from game.skills.skill_loader import ALL_SKILLS

    if not hasattr(player, "skills") or len(player.skills) == 0:
        print("You have no skills.")
        return None

    print("\nChoose a skill:")
    for i, skill_id in enumerate(player.skills, start=1):
        skill = ALL_SKILLS[skill_id]
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
