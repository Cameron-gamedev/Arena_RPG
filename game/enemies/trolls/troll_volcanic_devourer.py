from game.enemies.enemy import Enemy
import random

class TrollVolcanicDevourer(Enemy):
    def __init__(self, level):
        name = "Troll Volcanic Devourer"
        max_hp = int(100 * 2.0)     # 200 HP
        attack = int(13 * 1.5)      # 19 ATK
        defense = int(11 * 1.5)     # 16 DEF

        super().__init__(name, level, max_hp, attack, defense)

        self.hit_chance = 0.75
        self.dodge_chance = 0.05
        self.crit_chance = 0.10
        self.armor_defense = 4

        self.passive_hp_regen = 5

        self.is_boss = True
        self.is_elite = False


        self.enraged = False

        self.lava_slam = {
            "name": "Lava Slam",
            "damage": {"flat": 8, "scaling": {"attack": 0.60}, "hits": 1},
            "status_effects": [
                {"name": "Burn", "duration": 3, "data": {"amount_per_turn": 4}}
            ]
        }

        self.magma_breath = {
            "name": "Magma Breath",
            "skip": True,
            "status_effects": [
                {"name": "Burn", "duration": 4, "data": {"amount_per_turn": 5}},
                {"name": "Weaken", "duration": 2}
            ]
        }

        self.eruption = {
            "name": "Volcanic Eruption",
            "damage": {"flat": 10, "scaling": {"attack": 0.70}, "hits": 1},
            "status_effects": [
                {"name": "Burn", "duration": 3, "data": {"amount_per_turn": 6}}
            ]
        }

        self.breath_cd = 0
        self.eruption_cd = 0

    def choose_action(self, player, allies=None):
        if self.breath_cd > 0: self.breath_cd -= 1
        if self.eruption_cd > 0: self.eruption_cd -= 1

        if not self.enraged and self.current_hp <= self.max_hp * 0.50:
            self.enraged = True
            self.apply_status("Rage", "buff", 999, {"percent": 0.25})
            return self.magma_breath

        if self.eruption_cd == 0:
            self.eruption_cd = 4
            return self.eruption

        if self.breath_cd == 0 and random.random() < 0.40:
            self.breath_cd = 3
            return self.magma_breath

        return self.lava_slam
