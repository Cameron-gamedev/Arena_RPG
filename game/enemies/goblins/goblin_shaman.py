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

        # -------------------------
        # Basic Attack
        # -------------------------
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

        # -------------------------
        # Mend Flesh (Burst Heal)
        # -------------------------
        self.heal_cooldown = 0
        self.heal_ability = {
            "name": "Mend Flesh",
            "heal_percent": 0.20
        }

        # -------------------------
        # Regenerative Hex (HoT)
        # -------------------------
        self.hot_cooldown = 0
        self.hot_ability = {
            "name": "Regenerative Hex",
            "hot_effects": [
                {"name": "RegenHP", "duration": 3, "amount_per_turn": 3, "target": "ally"}
            ]
        }

        # -------------------------
        # Storm Channel (Delayed Burst)
        # -------------------------
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
                {"name": "Shock", "duration": 1, "stun_chance": 0.15}
            ]
        }

    def choose_action(self, player, allies=None):
        if allies is None:
            allies = []

        # -------------------------
        # Release Storm Channel
        # -------------------------
        if self.channeling:
            self.channeling = False
            self.channel_cooldown = 4
            return self.channel_ability

        # -------------------------
        # Cooldowns
        # -------------------------
        if self.channel_cooldown > 0:
            self.channel_cooldown -= 1
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        if self.hot_cooldown > 0:
            self.hot_cooldown -= 1

        # -------------------------
        # Healing Logic
        # -------------------------
        living_allies = [a for a in allies if not a.is_dead()]
        if living_allies:
            lowest = min(living_allies, key=lambda e: e.current_hp / e.max_hp)
            hp_ratio = lowest.current_hp / lowest.max_hp

            # Priority 1: Mend Flesh (emergency heal)
            if hp_ratio < 0.50 and self.heal_cooldown == 0:
                self.heal_cooldown = 3
                return {"name": "Mend Flesh", "heal_target": lowest}

            # Priority 2: Regenerative Hex (sustained heal)
            if hp_ratio < 0.70 and self.hot_cooldown == 0:
                self.hot_cooldown = 4
                return self.hot_ability

        # -------------------------
        # Begin Channeling (30% chance)
        # -------------------------
        if self.channel_cooldown == 0 and random.random() < 0.30:
            self.channeling = True
            print(f"{self.name} begins channeling storm energy!")
            return {"name": "Channeling", "skip": True}

        # -------------------------
        # Fallback: Hex Bolt
        # -------------------------
        return self.basic_attack