
from game.enemies.goblins.goblin_skirmisher import GoblinSkirmisher
from game.enemies.goblins.goblin_assassin import GoblinAssassin
from game.enemies.goblins.goblin_saboteur import GoblinSaboteur
from game.enemies.goblins.goblin_shaman import GoblinShaman
from game.enemies.goblins.goblin_shadowblade_saboteur import ShadowbladeSaboteur
from game.enemies.goblins.goblin_warlock_king import GoblinWarlockKing

from game.enemies.orcs.orc_brute import OrcBrute
from game.enemies.orcs.orc_grunt import OrcGrunt
from game.enemies.orcs.orc_berserker import OrcBerserker
from game.enemies.orcs.orc_warcaller import OrcWarcaller
from game.enemies.orcs.orc_ironbreaker_champion import OrcIronbreaker
from game.enemies.orcs.orc_doomcaller_warlord import OrcDoomcallerWarlord

from game.enemies.trolls.troll_bruiser import TrollBruiser
from game.enemies.trolls.troll_regenerator import TrollRegenerator
from game.enemies.trolls.troll_shaman import TrollShaman
from game.enemies.trolls.troll_firebelly import TrollFirebelly
from game.enemies.trolls.troll_boulderback import TrollBoulderback
from game.enemies.trolls.troll_volcanic_devourer import TrollVolcanicDevourer


ENEMY_REGISTRY = {
    "Goblin Skirmisher": GoblinSkirmisher,
    "Goblin Assassin": GoblinAssassin,
    "Goblin Saboteur": GoblinSaboteur,
    "Goblin Shaman": GoblinShaman,
    "Shadowblade Saboteur": ShadowbladeSaboteur,
    "Goblin Warlock-King": GoblinWarlockKing,

    "Orc Brute": OrcBrute,
    "Orc Grunt": OrcGrunt,
    "Orc Berserker": OrcBerserker,
    "Orc Warcaller": OrcWarcaller,
    "Orc Ironbreaker Champion": OrcIronbreaker,
    "Orc Doomcaller Warlord": OrcDoomcallerWarlord,

    "Troll Bruiser": TrollBruiser,
    "Troll Regenerator": TrollRegenerator,
    "Troll Shaman": TrollShaman,
    "Troll Firebelly": TrollFirebelly,
    "Troll Boulderback Crusher": TrollBoulderback,
    "Troll Volcanic Devourer": TrollVolcanicDevourer,
}


class EnemyFactory:

    @staticmethod
    def create(enemy_type: str, level: int):
        if enemy_type not in ENEMY_REGISTRY:
            raise ValueError(f"Unknown enemy type: {enemy_type}")

        enemy_class = ENEMY_REGISTRY[enemy_type]
        return enemy_class(level)

    @staticmethod
    def spawn_wave(enemy_list, wave_number, tier):
        enemies = []

        for entry in enemy_list:
            enemy_type = entry["type"]
            is_elite = entry.get("elite", False)
            is_boss = entry.get("boss", False)

            level = scale_enemy_level(
                wave_number,
                tier,
                is_elite=is_elite,
                is_boss=is_boss
            )

            enemy = EnemyFactory.create(enemy_type, level)
            enemies.append(enemy)

        return enemies



def scale_enemy_level(wave_number, tier, is_elite=False, is_boss=False):
    tier_offset = {
        "goblin": 0,
        "orc": 1,
        "troll": 2
    }.get(tier, 0)

    level = wave_number + tier_offset

    if is_elite:
        level += 1
    if is_boss:
        level += 2

    return level
