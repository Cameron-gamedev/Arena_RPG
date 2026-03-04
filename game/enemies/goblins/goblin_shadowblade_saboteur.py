from game.enemies.enemy import Enemy
import random

class ShadowbladeSaboteur(Enemy):
    def __init__(self, level):
        name = "Shadowblade Saboteur"
        max_hp = int(30 * 1.5)      # 45 HP
        attack = int(6 * 1.3)       # 7 ATK
        defense = int(2 * 1.3)      # 2 DEF

        super().__init__(name, level, max_hp, attack, defense)

        self.hit_chance = 0.85
        self.dodge_chance = 0.30
        self.crit_chance = 0.15

        self.is_boss = False
        self.is_elite = True


        self.shadow_stab = {
            "name": "Shadow Stab",
            "damage": {"flat": 5, "scaling": {"attack": 0.40}, "hits": 1},
            "status_effects": [{"name": "Weaken", "duration": 2}]
        }

        self.shrapnel_fan = {
            "name": "Shrapnel Fan",
            "damage": {"flat": 4, "scaling": {"attack": 0.30}, "hits": 2},
            "status_effects": [
                {"name": "Vulnerable", "duration": 2},
                {"name": "AccuracyDown", "duration": 2}
            ]
        }

        self.toxic_slash = {
            "name": "Toxic Slash",
            "damage": {"flat": 3, "scaling": {"attack": 0.25}, "hits": 1},
            "status_effects": [
                {"name": "Poison", "duration": 3, "data": {"amount_per_turn": 3}}
            ]
        }

        self.fan_cd = 0
        self.toxic_cd = 0

    def choose_action(self, player, allies=None):
        if self.fan_cd > 0: self.fan_cd -= 1
        if self.toxic_cd > 0: self.toxic_cd -= 1

        if self.fan_cd == 0 and random.random() < 0.35:
            self.fan_cd = 3
            return self.shrapnel_fan

        if self.toxic_cd == 0 and not player.has_status("Poison"):
            self.toxic_cd = 3
            return self.toxic_slash

        return self.shadow_stab
