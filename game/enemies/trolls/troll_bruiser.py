from game.enemies.enemy import Enemy
import random

class TrollBruiser(Enemy):
    def __init__(self, level):
        name = "Troll Bruiser"
        max_hp = 100
        attack = 13
        defense = 11
        super().__init__(name, level, max_hp, attack, defense)

        self.armor_defense = 3
        self.hit_chance = 0.65   
        self.crit_chance = 0.03
        self.dodge_chance = 0.05

        self.passive_hp_regen = 3
        self.passive_sp_regen = 1
        self.passive_mp_regen = 0

        self.base_attack = attack
        self.base_defense = defense
        self.base_hit = self.hit_chance
        self.base_crit = self.crit_chance
        self.base_dodge = self.dodge_chance

        self.basic_attack = {
            "name": "Crushing Fist",
            "damage": {
                "flat": 6,
                "scaling": {"attack": 0.60},
                "hits": 1
            },
            "status_effects": []
        }

        self.armor_shred = {
            "name": "Bonebreaker",
            "damage": {
                "flat": 4,
                "scaling": {"attack": 0.45},
                "hits": 1
            },
            "status_effects": [
                {"name": "Vulnerable", "duration": 2, "chance": 1.0}
            ]
        }
        
        self.thick_hide_used = False
        self.thick_hide = {
            "name": "Thick Hide",
            "skip": True,
            "status_effects": [
                {"name": "ThickHideDefense", "duration": 2, "target": "self"},
                {"name": "ThickHideArmor", "duration": 2, "target": "self"}
            ]
        }

        self.enrage_triggered = False

    def check_enrage(self):
        if self.enrage_triggered:
            return
        if self.current_hp <= self.max_hp * 0.50:
            self.enrage_triggered = True
            print(f"{self.name} roars as ancient power awakens!")

            # Convert all manual stat edits into status effects
            self.apply_status("Rage", "buff", 999, {"percent": 0.20})
            self.apply_status("ThickHideDefense", "buff", 999, {"flat": 2})
            self.apply_status("ThickHideArmor", "buff", 999, {"flat": 1})

    def choose_action(self, player, allies=None):
        if allies is None:
            allies = []

        self.check_enrage()

        if not self.thick_hide_used and not self.enrage_triggered:
            self.thick_hide_used = True
            return self.thick_hide
        
        if player.defense >= 12:
            return self.armor_shred
        
        if self.enrage_triggered:
            return self.basic_attack if random.random() < 0.70 else self.armor_shred
        
        return self.basic_attack if random.random() < 0.50 else self.armor_shred
