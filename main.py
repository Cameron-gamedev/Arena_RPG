from game.player import Player
from game.enemies.goblins.goblin_skirmisher import GoblinSkirmisher
from game.enemies.goblins.goblin_assassin import GoblinAssassin
from game.enemies.goblins.goblin_saboteur import GoblinSaboteur
from game.enemies.goblins.goblin_shaman import GoblinShaman
from game.enemies.orcs.orc_grunt import OrcGrunt
from game.enemies.orcs.orc_brute import OrcBrute
from game.enemies.orcs.orc_beserker import OrcBerserker
from game.enemies.orcs.orc_warcaller import OrcWarcaller
from game.enemies.trolls.troll_bruiser import TrollBruiser

from game.items.sample_items import (
    iron_sword,champions_gauntlets, 
    warriors_charm, minor_helath_potion, 
    rejuvenation_potion,strength_elixir
)
from game.combats.engine import CombatEngine

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

    player.skills = ["Fireball", "Cleave","ArcaneNova"]

    # Equip items
    player.equipment.equip_item("weapon_main", iron_sword)
    player.equipment.equip_item("armor", champions_gauntlets)
    player.equipment.equip_item("amulet", warriors_charm)

    player.inventory.add_item(minor_helath_potion)
    player.inventory.add_item(rejuvenation_potion)
    player.inventory.add_item(strength_elixir)

    # Recalculate stats
    player.recalculate_stats()

    # Print stats
    print("\n=== PLAYER STATS ===")
    print("Attack:", player.attack)
    print("Defense:", player.defense)
    print("Crit Chance:", player.crit_chance)
    print("Max HP:", player.max_hp)

    """engine = CombatEngine(player, waves=[
        [GoblinSkirmisher(),GoblinAssassin() ],
        [GoblinSkirmisher(),GoblinSaboteur() ],
        [GoblinSkirmisher(), GoblinShaman()],
        [GoblinSkirmisher(), GoblinAssassin(), GoblinSaboteur()]
    ])"""

    """engine = CombatEngine(player, waves=[
        [OrcGrunt(), OrcBrute()],
        [OrcGrunt(), OrcBerserker()],
        [OrcGrunt(), OrcWarcaller()]
    ])"""
    
    engine  = CombatEngine(player, waves=[
        [TrollBruiser()]
    ])
    engine.start_combat()


if __name__ == "__main__":
    main()
