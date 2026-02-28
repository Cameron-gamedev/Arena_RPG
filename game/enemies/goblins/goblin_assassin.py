from game.enemies.enemy import Enemy
import random

class GoblinAssassin(Enemy):
    def __init__(self):
        
        name = "Goblin Assassin"
        max_hp = 24
        attack = 8
        defense = 1

        super().__init__(name, max_hp, attack, defense)

        self.dodge_chance = 0.25
        self.hit_chance = 0.85
        self.crit_chance = 0.20

        self.basic_attack = {
            "name": "Twin Daggers",
            "damage": {
                "flat": 2,
                "scaling":{"attack":0.30},
                "hits":2
            },
            
            "status_effects":[],
            "second_hit_accuracy": 0.50
        }

        self.signature_cooldown = 0
        self.signature_ability = {
            "name":"Poisoned Blade",
            "damage":{
                "flat":6,
                "scaling":{"attack": 0.40},
                "hits":1
            },
            "status_effects":[
                {"name": "Poison", "duration": 3, "amount_per_turn": 4}
            ],
        }
        
        self.smoke_veil_used = False
        self.smoke_veil = {
            "name":"Smoke Veil",
            "buff":{
                "stat":"dodge_chance",
                "percent": 0.30
            }, 
            "duration": 2
        }

    def choose_action(self, player, allies=None):
        import random

        # --- 1. SMOKE VEIL TRIGGER (below 20% HP, once per combat) ---
        hp_ratio = self.current_hp / self.max_hp
        if hp_ratio < 0.25 and not self.smoke_veil_used:
            self.smoke_veil_used = True

            # Apply dodge buff to the Assassin
            self.apply_status(
                name="BuffDodgeChance",
                effect_type="buff",
                duration=self.smoke_veil["duration"],
                data={"percent": self.smoke_veil["buff"]["percent"]}
            )

            print(f"{self.name} vanishes into a Smoke Veil!")
            return {"name": "Smoke Veil", "skip": True}

        # --- 2. POISONED BLADE LOGIC (weighted + cooldown) ---
        if self.signature_cooldown > 0:
            self.signature_cooldown -= 1
        else:
            roll = random.random()
            if roll < 0.35:  # 30% chance
                self.signature_cooldown = 3
                return self.signature_ability

        # --- 3. FALLBACK: TWIN DAGGERS ---
        return self.basic_attack
