
from game.enemies.enemy import Enemy
import random

class GoblinSkirmisher(Enemy):
    def __init__(self):
        name = "Goblin Skirmisher"
        max_hp = 30
        attack = 6
        defense = 2
        
        super().__init__(name, max_hp, attack, defense)

        self.dodge_chance = 0.20
        self.hit_chance = 0.80
        self.crit_chance = 0.10

        self.basic_attack = {
            "name":"Quick Stab",
            "damage": {
                "flat":4,
                "scaling":{"attack":0.2}, # small scaling from enemy attack stat
                "hits":1
            },
            "status_effects":[] 
        }

        self.signature_cooldown = 0
        self.signature_abiliy = {
            "name":"Smoke Bomb",
            "damage":{
                "flat":0,
                "scaling":{},
                "hits":1
            },
            "status_effects":[
                {"name":"AccuracyDown", "duration":2}
            ]
        }

        self.panic_skip = {"name": "Panic", "skip":True}

        self.panic_weak_attack = {
            "name":"Shaky-Stab",
            "damage":{"flat": 2, "scaling":{"attack":0.1}, "hits":1},
            "status_effect":[]
        }

    def choose_action(self, player, allies=None):
        # --- 1. PANIC CHECK (highest priority) ---
        hp_ratio = self.current_hp / self.max_hp
        
        if hp_ratio <= 0.30:
            roll = random.random()
            if roll < 0.30:
                print(f"{self.name} panics and does nothing!")
                return self.panic_skip
            else:
                print(f"{self.name} weakly attacks...")
                return self.panic_weak_attack
            
        # --- 2. SMOKE BOMB LOGIC (weighted + cooldown) ---
        if self.signature_cooldown > 0:
            self.signature_cooldown -=1
        else:
            roll = random.random()
            if roll < 0.30:
                self.signature_cooldown = 3
                return self.signature_abiliy
            
        # --- 3. FALLBACK: QUICK STAB ---
        return self.basic_attack