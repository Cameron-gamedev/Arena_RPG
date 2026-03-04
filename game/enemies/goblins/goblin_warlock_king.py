from game.enemies.enemy import Enemy
import random

class GoblinWarlockKing(Enemy):
    def __init__(self, level):
        name = "Goblin Warlock-King"
        max_hp = int(30 * 2.0)      # 60 HP
        attack = int(6 * 1.5)       # 9 ATK
        defense = int(2 * 1.5)      # 3 DEF

        super().__init__(name, level, max_hp, attack, defense)

        self.hit_chance = 0.90
        self.dodge_chance = 0.30
        self.crit_chance = 0.20

        self.is_boss = True
        self.is_elite = False


        self.hex_bolt = {
            "name": "Hex Bolt",
            "damage": {"flat": 5, "scaling": {"attack": 0.40}, "hits": 1},
            "status_effects": [
                {"name": "Weaken", "duration": 2},
                {"name": "AccuracyDown", "duration": 2}
            ]
        }

        self.curse_of_ruin = {
            "name": "Curse of Ruin",
            "skip": True,
            "status_effects": [
                {"name": "Poison", "duration": 3, "data": {"amount_per_turn": 4}},
                {"name": "Vulnerable", "duration": 2},
                {"name": "Slow", "duration": 2}
            ]
        }

        self.dark_command = {
            "name": "Dark Command",
            "skip": True,
            "status_effects": [
                {"name": "Weaken", "duration": 2},
                {"name": "AccuracyDown", "duration": 2}
            ]
        }

        self.curse_cd = 0
        self.command_cd = 0

    def choose_action(self, player, allies=None):
        if self.curse_cd > 0: self.curse_cd -= 1
        if self.command_cd > 0: self.command_cd -= 1

        if self.curse_cd == 0:
            self.curse_cd = 4
            return self.curse_of_ruin

        if self.command_cd == 0 and random.random() < 0.40:
            self.command_cd = 3
            return self.dark_command

        return self.hex_bolt
