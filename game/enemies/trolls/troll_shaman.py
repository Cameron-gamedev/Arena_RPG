from game.enemies.enemy import Enemy
import random

class TrollShaman(Enemy):
    def __init__(self):
        name = "Troll Shaman"
        max_hp = 80
        attack = 8
        defense = 9

        super().__init__(name, max_hp, attack, defense)

        self.armor_defense = 2
        self.hit_chance = 0.70
        self.crit_chance = 0.05
        self.dodge_chance = 0.03

        self.passive_hp_regen = 2
        self.passive_mp_regen = 2
        self.passive_sp_regen = 1

        self.rotting_hex = {
            "name": "Rotting Hex",
            "skip": True,
            "status_effects": [
                {
                    "name": "Poison",
                    "duration": 3,
                    "target": "player",
                    "data": {"amount_per_turn": 3}
                },
                {
                    "name": "Weaken",
                    "duration": 3,
                    "target": "player",
                    "data": {"percent": 0.15}
                }
            ]
        }

        self.spirit_drain = {
            "name": "Spirit Drain",
            "skip": True,
            "custom_effects": [
                {
                    "type": "drain_resources",
                    "sp_amount": 3,
                    "mp_amount": 3,
                    "self_sp_restore": 2,
                    "self_mp_restore": 1
                }
            ],
            "status_effects": [
                {
                    "name": "Weaken",
                    "duration": 2,
                    "target": "player",
                    "data": {"percent": 0.10}
                }
            ]
        }

        self.earthbind = {
            "name": "Earthbind",
            "skip": True,
            "status_effects": [
                {"name": "Intimidate", "duration": 2, "target": "player"},
                {"name": "DodgeDown", "duration": 2, "target": "player", "data": {"percent": -0.05}},
                {"name": "BuffHitChance", "duration": 2, "target": "self", "data": {"percent": 0.10}},
                {"name": "BuffDodgeChance", "duration": 2, "target": "self", "data": {"percent": 0.05}}
            ]
        }

    def choose_action(self, player, allies=None):
        if allies is None:
            allies = []

        def has_status(name):
            return player.has_status(name)

        if not has_status("Poison") or not has_status("Weaken"):
            return self.rotting_hex

        if player.hit_chance > 0.85 or player.dodge_chance > 0.05:
            return self.earthbind

        if player.current_sp > player.max_sp * 0.30 or player.current_mp > player.max_mp * 0.30:
            return self.spirit_drain

        return self.rotting_hex
