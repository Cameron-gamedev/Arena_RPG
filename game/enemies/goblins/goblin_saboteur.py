from game.enemies.enemy import Enemy
import random

class GoblinSaboteur(Enemy):
    def __init__(self):
        name = "Goblin Saboteur"
        max_hp = 25
        attack = 5
        defense = 1

        super().__init__(name, max_hp, attack, defense)

        self.dodge_chance = 0.25
        self.hit_chance = 0.80
        self.crit_chance = 0.10

        self.basic_attack = {
            "name": "Crippling Jab",
            "damage": {
                "flat": 4,
                "scaling": {"attack": 0.25},
                "hits": 1
            },
            "status_effects": [
                {"name": "Weaken", "duration": 2}
            ]
        }

        self.signature_cooldown = 0
        self.signature_ability = {
            "name": "Shrapnel Bomb",
            "damage": {
                "flat": 6,
                "scaling": {"attack": 0.30},
                "hits": 1
            },
            "status_effects": [
                {"name": "Vulnerable", "duration": 2},
                {"name": "Slow", "duration": 2}
            ]
        }

        self.condition_used = False
        self.conditional_ability = {
            "name": "Toxic Flask",
            "skip": True,
            "status_effects": [
                {"name": "Poison", "duration": 3, "data": {"amount_per_turn": 3}},
                {"name": "AccuracyDown", "duration": 2}
            ]
        }

    def choose_action(self, player, allies=None):
        hp_ratio = self.current_hp / self.max_hp
        print(f"[AI DEBUG] HP ratio: {hp_ratio:.2f}, condition_used={self.condition_used}, sig_cd={self.signature_cooldown}")

        if hp_ratio < 0.30 and not self.condition_used:
            self.condition_used = True
            print(f"{self.name} hurls a Toxic Flask!")
            return self.conditional_ability

        if self.signature_cooldown > 0:
            self.signature_cooldown -= 1
        else:
            if random.random() < 0.40:
                self.signature_cooldown = 3
                return self.signature_ability
            
        return self.basic_attack
