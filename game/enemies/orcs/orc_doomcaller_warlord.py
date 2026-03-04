from game.enemies.enemy import Enemy
import random

class OrcDoomcallerWarlord(Enemy):
    def __init__(self, level):
        name = "Orc Doomcaller Warlord"
        max_hp = int(55 * 2.0)      # 110 HP
        attack = int(10 * 1.5)      # 15 ATK
        defense = int(8 * 1.5)      # 12 DEF

        super().__init__(name, level, max_hp, attack, defense)

        self.hit_chance = 0.90
        self.dodge_chance = 0.05
        self.crit_chance = 0.15
        self.armor_defense = 3

        self.is_boss = True
        self.is_elite = False


        self.enraged = False

        self.warlord_strike = {
            "name": "Warlord Strike",
            "damage": {"flat": 7, "scaling": {"attack": 0.60}, "hits": 1},
            "status_effects": []
        }

        self.staggering_blow = {
            "name": "Staggering Blow",
            "damage": {"flat": 5, "scaling": {"attack": 0.50}, "hits": 1},
            "status_effects": [{"name": "Stagger", "duration": 1}]
        }

        self.warcry = {"name": "Warcry", "skip": True}

        self.warcry_cd = 0

    def choose_action(self, player, allies=None):
        if self.warcry_cd > 0: self.warcry_cd -= 1

        if not self.enraged and self.current_hp <= self.max_hp * 0.50:
            self.enraged = True
            self.apply_status("Rage", "buff", 999, {"percent": 0.25})
            return self.warcry

        if self.warcry_cd == 0:
            self.warcry_cd = 4
            return self.warcry

        if random.random() < 0.40:
            return self.staggering_blow

        return self.warlord_strike
