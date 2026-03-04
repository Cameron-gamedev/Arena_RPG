from game.enemies.enemy import Enemy
import random

class OrcBerserker(Enemy):
    def __init__(self, level):
        name = "Orc Berserker"
        max_hp = 42
        attack = 12
        defense = 4

        super().__init__(name, level, max_hp, attack, defense)

        self.hit_chance = 0.85
        self.dodge_chance = 0.08
        self.crit_chance = 0.20
        self.armor_defense = 1

        self.base_attack = attack
        self.base_defense = defense
        self.base_hit = self.hit_chance
        self.base_dodge = self.dodge_chance
        self.base_crit = self.crit_chance

        self.passive_hp_regen = 0
        self.passive_mp_regen = 0
        self.passive_sp_regen = 2

        self.frenzy_triggered = False
        self.blood_frenzy_used = False

        self.wild_slash = {
            "name": "Wild Slash",
            "damage": {"flat": 2, "scaling": {"attack": 0.30}, "hits": 3},
            "second_hit_accuracy": 0.70,
            "third_hit_accuracy": 0.50,
            "status_effects": []
        }

        self.blood_frenzy = {"name": "Blood Frenzy", "skip": True}

        self.reckless_charge = {
            "name": "Reckless Charge",
            "damage": {"flat": 8, "scaling": {"attack": 0.60}, "hits": 1},
            "self_damage": 5,
            "status_effects": []
        }

    def choose_action(self, player, allies=None):
        if not self.frenzy_triggered and self.current_hp <= self.max_hp * 0.50:
            self.frenzy_triggered = True
            print(f"{self.name} enters a violent Frenzy!")

            self.apply_status("Rage", "buff", 999, {"percent": 0.25})
            self.apply_status("BuffCritChance", "buff", 999, {"percent": 0.15})
            self.apply_status("GuardBreak", "debuff", 2, {})

            self.passive_sp_regen += 1
            return {"name": "Frenzy", "skip": True}

        if not self.blood_frenzy_used:
            self.blood_frenzy_used = True
            print(f"{self.name} whips itself into a Blood Frenzy!")
            self.apply_status("BattleFury", "buff", 3, {"percent": 0.20})
            return self.blood_frenzy

        if self.current_hp <= self.max_hp * 0.30 and random.random() < 0.50:
            print(f"{self.name} charges recklessly!")
            return self.reckless_charge

        return self.wild_slash
