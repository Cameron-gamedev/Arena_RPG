import random
from game.enemies.enemy import Enemy

class TrollRegenerator(Enemy):
    def __init__(self, level):
        name = "Troll Regenerator"
        max_hp = 90
        attack = 10
        defense = 10
        armor_defense = 3

        super().__init__(name, level, max_hp, attack, defense)

        self.armor_defense = armor_defense
        self.hit_chance = 0.65
        self.dodge_chance = 0.02
        self.crit_chance = 0.05

        self.passive_hp_regen = 4
        self.passive_sp_regen = 1
        self.passive_mp_regen = 0

        self.base_attack = attack
        self.base_defense = defense
        self.base_hit = self.hit_chance
        self.base_dodge = self.dodge_chance
        self.base_crit = self.crit_chance

        self.mend_flesh = {
            "name": "Mend Flesh",
            "skip": True,
            "hot_effects": [
                {
                    "name": "RegenHP",
                    "duration": 3,
                    "amount_per_turn": 4,
                    "target": "ally"
                }
            ]
        }

        self.vital_sap = {
            "name": "Vital Sap",
            "damage": {
                "flat": 3,
                "scaling": {"attack": 0.35},
                "hits": 1
            },
            "status_effects": [
                {
                    "name": "RegenHP",
                    "duration": 2,
                    "target": "self",
                    "data": {"amount_per_turn": 3}
                },
                {
                    "name": "Bleed",
                    "duration": 2,
                    "target": "player",
                    "data": {"amount_per_turn": 3, "stacking": "refresh"}
                }
            ]
        }

        self.consume_essence = {
            "name": "Consume Essence",
            "skip": True,
            "heal_percent": 0.25,
            "status_effects": [
                {"name": "EssenceDefense", "duration": 2}
            ]
        }

    def choose_action(self, player, allies=None):
        if allies is None:
            allies = []

        living_allies = [a for a in allies if not a.is_dead() and a is not self]
        dead_allies = [a for a in allies if a.is_dead() and a is not self]

        if dead_allies:
            return self.consume_essence

        if living_allies:
            lowest = min(living_allies, key=lambda a: a.current_hp / a.max_hp)
            if lowest.current_hp <= lowest.max_hp * 0.50:
                return self.mend_flesh

        if not living_allies and self.current_hp <= self.max_hp * 0.60:
            return self.mend_flesh

        return self.vital_sap
