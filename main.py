from game.player import Player
from game.items.sample_items import (
    iron_sword, champions_gauntlets, warriors_charm,
    minor_helath_potion, rejuvenation_potion, strength_elixir
)
from game.combats.engine import CombatEngine
from game.waves.wave_manager import WaveManager


def choose_player_class():
    class_options = ["Warrior", "Wizard", "Ranger", "Cleric"]

    print("\nChoose your class:")
    for i, class_name in enumerate(class_options, start=1):
        print(f" {i}. {class_name}")

    while True:
        choice = input("Class (number or name): ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(class_options):
                return class_options[idx]

        normalized = choice.lower()
        for class_name in class_options:
            if normalized == class_name.lower():
                return class_name

        print("Invalid class. Please choose Warrior, Wizard, Ranger, or Cleric.")


def main():
    player = Player(
        name="Hero",
        strength=10,
        agility=10,
        vitality=10,
        intelligence=5,
        base_atk=5,
        base_def=5
    )

    # Set class
    selected_class = choose_player_class()
    player.set_class(selected_class)

    # Equip items
    player.equipment.equip_item("weapon_main", iron_sword)
    player.equipment.equip_item("armor", champions_gauntlets)
    player.equipment.equip_item("amulet", warriors_charm)

    # Add consumables
    player.inventory.add_item(minor_helath_potion)
    player.inventory.add_item(rejuvenation_potion)
    player.inventory.add_item(strength_elixir)

    # Recalculate stats
    player.recalculate_stats()

    print("\n=== PLAYER READY ===")
    print(f"Class: {player.player_class_name}")
    print(f"Level: {player.level}")
    print(f"Attack: {player.attack}")
    print(f"Defense: {player.defense}")
    print(f"Max HP: {player.max_hp}")

    # Start the wave run
    wave_manager = WaveManager(player, CombatEngine)
    wave_manager.start_run()


if __name__ == "__main__":
    main()
