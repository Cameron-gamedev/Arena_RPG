from game.enemies.enemy import Enemy
import random

class GoblinAssassin(Enemy):
    def __init__(self):
        name = "Goblin Assassin"
        max_hp = 24
        attack = 8
        defense = 1

        super().__init__(name, max_hp, attack, defense)

        self.dodge_chance = 0.25
        self.hit_chance = 0.85
        self.crit_chance = 0.20

        self.basic_attack = {
            "name": "Twin Daggers",
            "damage": {
                "flat": 2,
                "scaling": {"attack": 0.30},
                "hits": 2
            },
            "status_effects": [],
            "second_hit_accuracy": 0.45
        }

        self.signature_cooldown = 0
        self.signature_ability = {
            "name": "Poisoned Blade",
            "damage": {
                "flat": 6,
                "scaling": {"attack": 0.40},
                "hits": 1
            },
            "status_effects": [
                {"name": "Poison", "duration": 3, "data": {"amount_per_turn": 4}}
            ]
        }
        
        self.smoke_veil_used = False
        self.smoke_veil = {
            "name": "Smoke Veil",
            "skip": True,
            "status_effects": [
                {"name": "BuffDodgeChance", "duration": 2, "data": {"percent": 0.30}, "target": "self"}
            ]
        }

    def choose_action(self, player, allies=None):
        hp_ratio = self.current_hp / self.max_hp

        if hp_ratio < 0.25 and not self.smoke_veil_used:
            self.smoke_veil_used = True
            print(f"{self.name} vanishes into a Smoke Veil!")
            return self.smoke_veil

        if self.signature_cooldown > 0:
            self.signature_cooldown -= 1
        else:
            if random.random() < 0.35:
                self.signature_cooldown = 3
                return self.signature_ability

        return self.basic_attack
