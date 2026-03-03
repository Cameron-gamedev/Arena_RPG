from game.enemies.enemy import Enemy
import random

class GoblinShaman(Enemy):
    def __init__(self):
        name = "Goblin Shaman"
        max_hp = 25
        attack = 4
        defense = 0

        super().__init__(name, max_hp, attack, defense)

        self.dodge_chance = 0.10
        self.hit_chance = 0.85
        self.crit_chance = 0.05

        self.basic_attack = {
            "name": "Hex Bolt",
            "damage": {
                "flat": 3,
                "scaling": {"attack": 0.30},
                "hits": 1
            },
            "status_effects": [
                {"name": "AccuracyDown", "duration": 1, "chance": 0.25}
            ]
        }

        self.heal_cooldown = 0
        self.heal_ability = {
            "name": "Mend Flesh",
            "skip": True,
            "hot_effects": [
                {"name": "RegenHP", "duration": 2, "amount_per_turn": 4, "target": "ally"}
            ]
        }

        self.channeling = False
        self.channel_cooldown = 0

        self.channel_ability = {
            "name": "Storm Channel",
            "damage": {
                "flat": 8,
                "scaling": {"attack": 0.40},
                "hits": 1
            },
            "status_effects": [
                {"name": "Shock", "duration": 1}
            ]
        }

    def choose_action(self, player, allies=None):
        if allies is None:
            allies = []

        if self.channeling:
            self.channeling = False
            self.channel_cooldown = 4
            return self.channel_ability

        if self.channel_cooldown > 0:
            self.channel_cooldown -= 1
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1

        living_allies = [a for a in allies if not a.is_dead()]
        if self.heal_cooldown == 0 and living_allies:
            low_ally = min(living_allies, key=lambda e: e.current_hp / e.max_hp)
            if (low_ally.current_hp / low_ally.max_hp) < 0.50:
                self.heal_cooldown = 3
                return {"name": "Mend Flesh", "heal_target": low_ally}

        if self.channel_cooldown == 0 and random.random() < 0.30:
            self.channeling = True
            print(f"{self.name} begins channeling storm energy!")
            return {"name": "Channeling", "skip": True}

        return self.basic_attack
