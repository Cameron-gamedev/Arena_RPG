from game.enemies.enemy import Enemy
import random

class TrollFirebelly(Enemy):
    def __init__(self, level):
        name = "Troll Firebelly"
        max_hp = 95
        attack = 12
        defense = 9
        super().__init__(name, level, max_hp, attack, defense)

        self.armor_defense = 2
        self.hit_chance = 0.65
        self.dodge_chance = 0.03
        self.crit_chance = 0.05

        self.ash_cooldown = 0

        self.smoldering_breath = {
            "name": "Smoldering Breath",
            "skip": True,
            "status_effects": [
                {
                    "name": "Burn",
                    "duration": 3,
                    "target": "player",
                    "data": {"amount_per_turn": 6}
                }
            ]
        }

        self.cinder_slam = {
            "name": "Cinder Slam",
            "damage": {
                "flat": 6,
                "scaling": {"attack": 0.40},
                "hits": 1
            },
            "status_effects": [
                {
                    "name": "Burn",
                    "duration": 3,
                    "target": "player",
                    "data": {"amount_per_turn": 4}
                }
            ]
        }

        self.ash_cloud = {
            "name": "Ash Cloud",
            "skip": True,
            "status_effects": [
                {"name": "AshenVeil", "duration": 2, "target": "player"}
            ]
        }

    def choose_action(self, player, allies=None):
        if self.ash_cooldown > 0:
            self.ash_cooldown -= 1

        if not player.has_status("Burn"):
            if random.random() < 0.70:
                return self.smoldering_breath

        if self.ash_cooldown == 0 and random.random() < 0.25:
            self.ash_cooldown = 3
            return self.ash_cloud

        return self.cinder_slam
