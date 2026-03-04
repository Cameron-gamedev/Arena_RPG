from game.enemies.enemy import Enemy
import random

class OrcGrunt(Enemy):
    def __init__(self, level):
        name = "Orc Grunt"
        max_hp = 55
        attack = 10
        defense = 8

        super().__init__(name, level, max_hp, attack, defense)

        self.hit_chance = 0.80
        self.dodge_chance = 0.05
        self.crit_chance = 0.05
        self.armor_defense = 2

        self.base_attack = attack
        self.base_defense = defense
        self.base_hit = self.hit_chance
        self.base_dodge = self.dodge_chance
        self.base_crit = self.crit_chance

        self.passive_hp_regen = 0
        self.passive_mp_regen = 0
        self.passive_sp_regen = 1

        self.heavy_swing = {
            "name": "Heavy Swing",
            "damage": {"flat": 4, "scaling": {"attack": 0.40}, "hits": 1},
            "status_effects": []
        }

        self.shield_bash = {
            "name": "Shield Bash",
            "damage": {"flat": 2, "scaling": {"attack": 0.20}, "hits": 1},
            "status_effects": [
                {"name": "Stagger", "duration": 1, "chance": 0.30}
            ]
        }

        self.battle_roar = {"name": "Battle Roar", "skip": True}

    def choose_action(self, player, allies=None):
        if not self.has_status("BattleFury"):
            self.apply_status("BattleFury", "buff", 2, {"percent": 0.20})
            print(f"{self.name} lets out a thunderous Battle Roar!")
            return self.battle_roar

        if player.has_status("BattleFury") or player.dodge_chance > 0.15:
            return self.shield_bash

        return self.heavy_swing
