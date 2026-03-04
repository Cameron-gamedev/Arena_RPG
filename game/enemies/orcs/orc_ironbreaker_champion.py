from game.enemies.enemy import Enemy
import random

class OrcIronbreaker(Enemy):
    def __init__(self, level):
        name = "Orc Ironbreaker"
        max_hp = int(55 * 1.5)      # 82 HP
        attack = int(10 * 1.3)      # 13 ATK
        defense = int(8 * 1.3)      # 10 DEF

        super().__init__(name, level, max_hp, attack, defense)

        self.hit_chance = 0.85
        self.dodge_chance = 0.05
        self.crit_chance = 0.10
        self.armor_defense = 3

        self.is_boss = False
        self.is_elite = True


        self.shield_crush = {
            "name": "Shield Crush",
            "damage": {"flat": 6, "scaling": {"attack": 0.50}, "hits": 1},
            "status_effects": [{"name": "Stagger", "duration": 1}]
        }

        self.armor_shatter = {
            "name": "Armor Shatter",
            "damage": {"flat": 4, "scaling": {"attack": 0.40}, "hits": 1},
            "status_effects": [{"name": "ArmorShatter", "duration": 2}]
        }

        self.battle_slam = {
            "name": "Battle Slam",
            "damage": {"flat": 8, "scaling": {"attack": 0.60}, "hits": 1},
            "status_effects": []
        }

        self.shatter_cd = 0

    def choose_action(self, player, allies=None):
        if self.shatter_cd > 0: self.shatter_cd -= 1

        if player.armor_defense > 0 and self.shatter_cd == 0:
            self.shatter_cd = 3
            return self.armor_shatter

        if random.random() < 0.40:
            return self.shield_crush

        return self.battle_slam
