
from game.enemies.enemy import Enemy
import random

class OrcBrute(Enemy):
    def __init__(self):
        name = "Orc Brute"
        max_hp = 75
        attack = 14
        defense = 10

        super().__init__(name, max_hp, attack, defense)

        self.hit_chance = 0.70
        self.dodge_chance = 0.03
        self.crit_chance = 0.10
        self.armor_defense = 3

        self.base_attack = attack
        self.base_defense = defense
        self.base_hit = self.hit_chance
        self.base_dodge = self.dodge_chance
        self.base_crit = self.crit_chance

        self.passive_hp_regen = 0
        self.passive_mp_regen = 0
        self.passive_sp_regen = 1

        self.is_winding_up = False
        self.rage_triggered = False

        self.heavy_slam = {
            "name": "Heavy Slam",
            "damage": {"flat": 6, "scaling": {"attack": 0.50}, "hits": 1}
        }

        self.winding_up = {"name": "Winding Up", "skip": True}

        self.crushing_blow = {
            "name": "Crushing Blow",
            "damage": {"flat": 12, "scaling": {"attack": 0.90}, "hits": 1}
        }

    def choose_action(self, player, allies=None):
        if not self.rage_triggered and self.current_hp <= self.max_hp * 0.50:
            self.rage_triggered = True
            print(f"{self.name} enters a furious RAGE!")

            self.apply_status("Rage", "buff", 999, {"flat": 0, "percent": 0.25})
            self.apply_status("BuffCritChance", "buff", 999, {"flat": 0.10})
            self.apply_status("GuardBreak", "debuff", 2, {})

            return {"name": "Rage", "skip": True}

        if self.is_winding_up:
            self.is_winding_up = False
            print(f"{self.name} unleashes a devastating Crushing Blow!")
            return self.crushing_blow

        if random.random() < 0.35:
            self.is_winding_up = True
            print(f"{self.name} begins winding up a massive attack!")
            return self.winding_up

        return self.heavy_slam