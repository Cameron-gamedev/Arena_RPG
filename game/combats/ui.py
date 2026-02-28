from game.combats.status import list_status_effects

def player_choose_action():
    print("\nChoose an action:")
    print(" 1. Attack")
    print(" 2. Skills")
    print(" 3. Items")
  
    while True:
        choice = input("Action number: ").strip()

        if choice == "1":
            return "attack"
        elif choice == "2":
            return "skills"
        elif choice == "3":
            return "items"
        else:
            print("Invalid choice. Try again.")


def display_health(player, enemies):
    print(f"{player.name}: {player.current_hp}/{player.max_hp} HP")
    for enemy in enemies:
        print(f"{enemy.name}: {enemy.current_hp}/{enemy.max_hp} HP")
    print("=" * 30)


def display_status(player, enemies):
    print(f"{player.name}: {player.current_hp}/{player.max_hp} HP")
    print(f"MP: {player.current_mp}/{player.max_mp} | SP: {player.current_sp}/{player.max_sp}")
    print(f"Status: {list_status_effects(player)}")

    for enemy in enemies:
        status = "DEAD" if enemy.is_dead() else f"{enemy.current_hp}/{enemy.max_hp} HP"
        print(f"{enemy.name}: {status}")
        if not enemy.is_dead():
            print(f" Status: {list_status_effects(enemy)}")

    print("=" * 30)

