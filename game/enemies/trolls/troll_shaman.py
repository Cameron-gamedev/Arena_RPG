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

        self.base_attack = attack
        self.base_defense = defense
        self.base_hit = self.hit_chance
        self.base_crit = self.crit_chance
        self.base_dodge = self.dodge_chance

        self.rotting_hex = {
            "name":"Rotting hex",
            "skip":True,
            "damage": None,
            "status_effects":[
                {
                    "name": "Poison",
                    "duration": 3,
                    "chance": 1.0,
                    "data": {"amount_per_turn":3},
                    "target": "player"
                },
                {
                    "name": "Weaken",
                    "duration": 3,
                    "chance": 1.0,
                    "data": {"percent": 0.15},
                    "target": "player"
                },
            ]
        }

        self.spirit_drain = {
            "name": "Spirit Drain",
            "skip": True,
            "damage": None,  # no direct damage
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
                    "chance": 1.0,
                    "data": {"percent": 0.10},
                    "target": "player"
                }
            ]
        }

        self.earthbind = {
            "name": "Earthbind",
            "skip":True,
            "damage": None,
            "status_effects": [
                {
                    "name": "Intimidate",       # reduces hit chance by 10%
                    "duration": 2,
                    "chance": 1.0,
                    "target": "player"
                },
                {
                    "name": "DodgeDown",        # reduces dodge chance by 5%
                    "duration": 2,
                    "chance": 1.0,
                    "data": {"percent": -0.05},
                    "target": "player"
                },
                {
                    "name": "BuffHitChance",    # increases Shaman hit chance by 10%
                    "duration": 2,
                    "chance": 1.0,
                    "data": {"percent": 0.10},
                    "target": "self"
                },
                {
                    "name": "BuffDodgeChance",  # increases Shaman dodge chance by 5%
                    "duration": 2,
                    "chance": 1.0,
                    "data": {"percent": 0.05},
                    "target": "self"
                }
            ]
        }

    def choose_action(self, player, allies=None):
        if allies is None:
            allies = []

        # Helper: check if player already has a status
        def has_status(name):
            return any(se["name"] == name for se in player.status_effects)

        # ============================================
        # 1. Ensure Rotting Hex is active
        # ============================================
        if not has_status("Poison") or not has_status("Weaken"):
            return self.rotting_hex

        # ============================================
        # 2. Control the battlefield with Earthbind
        # If player accuracy or dodge is still high
        # ============================================
        if player.hit_chance > 0.85 or player.dodge_chance > 0.05:
            return self.earthbind

        # ============================================
        # 3. Drain resources if player is still healthy
        # ============================================
        if player.current_sp > player.max_sp * 0.30 or player.current_mp > player.max_mp * 0.30:
            return self.spirit_drain

        # ============================================
        # 4. Default: maintain Rotting Hex
        # ============================================
        return self.rotting_hex
