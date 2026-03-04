from game.enemies.enemy import Enemy
import random

class TrollBoulderback(Enemy):
    def __init__(self, level):
        name = "Troll Boulderback"
        max_hp = int(100 * 1.5)     # 150 HP
        attack = int(13 * 1.3)      # 16 ATK
        defense = int(11 * 1.3)     # 14 DEF

        super().__init__(name, level, max_hp, attack, defense)

        self.hit_chance = 0.70
        self.dodge_chance = 0.05
        self.crit_chance = 0.05
        self.armor_defense = 4

        self.passive_hp_regen = 4

        self.is_boss = False
        self.is_elite = True


        self.boulder_fist = {
            "name": "Boulder Fist",
            "damage": {"flat": 7, "scaling": {"attack": 0.60}, "hits": 1},
            "status_effects": []
        }

        self.earth_shock = {
            "name": "Earth Shock",
            "damage": {"flat": 5, "scaling": {"attack": 0.40}, "hits": 1},
            "status_effects": [{"name": "Stun", "duration": 1}]
        }

        self.thick_hide = {
            "name": "Thick Hide",
            "skip": True,
            "status_effects": [
                {"name": "ThickHideDefense", "duration": 3, "target": "self"},
                {"name": "ThickHideArmor", "duration": 3, "target": "self"}
            ]
        }

        self.hide_used = False

    def choose_action(self, player, allies=None):
        if not self.hide_used and self.current_hp < self.max_hp * 0.60:
            self.hide_used = True
            return self.thick_hide

        if random.random() < 0.35:
            return self.earth_shock

        return self.boulder_fist
