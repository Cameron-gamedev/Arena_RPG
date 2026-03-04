from game.player import Player
from game.items.sample_items import (
    iron_sword, champions_gauntlets, warriors_charm,
    minor_helath_potion, rejuvenation_potion, strength_elixir
)
from game.combats.engine import CombatEngine
from game.waves.wave_manager import WaveManager


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

    # Set class (IMPORTANT)
    player.set_class("Warrior")  # or Wizard, Ranger, Cleric

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
