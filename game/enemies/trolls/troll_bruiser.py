from game.enemies.enemy import Enemy
import random

class TrollBruiser(Enemy):
    def __init__(self):
        name = "Troll Bruiser"
        max_hp = 100
        attack = 13
        defense = 11
        super().__init__(name, max_hp, attack, defense)

        self.armor_defense = 3
        self.hit_chance = 65
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
            "damage":{
                "flat":6,
                "scaling":{"attack":0.60},
                "hits":1
            },
            "status_effects":[]
        }

        self.armor_shred = {
            "name": "Bonebreaker",
            "damage":{
                "flat":4,
                "scaling":{"attack":0.45},
                "hits":1
            },
            "status_effects":[
                {"name": "Vulnerable", "duration":2, "chance":1.0}
            ]
        }
        
        self.thick_hide_used = False
        self.thick_hide = {
            "name": "Thick Hide",
            "skip": True,
            "status_effects": [
                {"name": "ThickHideDefense", "duration": 2, "target":"self"},
                {"name": "ThickHideArmor", "duration": 2, "target":"self"}
            ]
        }

        self.enrage_triggered =False

    
    def check_enrage(self):
        if self.enrage_triggered:
            return
        if self.current_hp <= self.max_hp *0.50:
            self.enrage_triggered = True

            print(f"{self.name} roars as ancient power awakens!")

            self.passive_hp_regen += 3
            self.defense += 2
            self.attack = int(self.attack * 1.20) # +20% attack
            self.armor_defense += 1

    
    def choose_action(self, player, allies=None):
        if allies is None:
            allies = []

        # Enrage check
        self.check_enrage()

        if not self.thick_hide_used and not self.enrage_triggered:
            self.thick_hide_used = True
            return self.thick_hide
        
        # If the player has high defense, prioritize Bonebreaker
        if player.defense >= 12: 
            return self.armor_shred
        
        # If enraged, prefer Crushing Fist
        if self.enrage_triggered:
            enrage_roll = random.random()
            if enrage_roll < 0.70:
                return self.basic_attack
            return self.armor_shred
        
        # Pre-enrage behavior
        action_roll = random.random()
        if action_roll < 0.50:
            return self.basic_attack
        else:
            return self.armor_shred
