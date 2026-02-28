import random
from game.status.status_definitions import STATUS_DEFINITIONS

class Enemy:
    def __init__(self, name, max_hp, attack, defense):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense

        self.max_sp = 35
        self.current_sp = self.max_sp
        
        self.max_mp = 35
        self.current_mp = self.max_mp
    
        
        self.dodge_chance = 0.25
        self.hit_chance = 0.0
        self.crit_chance = 0.15
        self.armor_defense = 0

        self.base_attack = attack
        self.base_defense = defense
        self.base_hit = self.hit_chance
        self.base_dodge = self.dodge_chance
        self.base_crit = self.crit_chance

        # Passive regen (default: none)
        self.passive_hp_regen = 0
        self.passive_mp_regen = 0
        self.passive_sp_regen = 0

        self.status_effects = []

        self.attack_profile = {}
        
    
    def choose_action(self, player, allies=None):
         return self.attack_profile

    
    def take_damage(self, amount):
        self.current_hp = max(0, self.current_hp - amount)
        #print(f"{self.name} takes {amount} damage (HP {self.current_hp}/{self.max_hp}).")


    def is_dead(self):
        return self.current_hp <= 0


    def can_attack(self):
        for effect in self.status_effects:
            if effect.get("type") == "stun" and effect.get("duration", 0) > 0:
                return False
        return True


    def apply_status(self, name, effect_type, duration, data=None):
        if data is None:
            data = {}

        definition = STATUS_DEFINITIONS.get(name)
        if definition is None:
            print(f"[Warning] Unknown status '{name}' attempted on {self.name}. Ignored.")
            return

        stacking = definition.get("stacking", "refresh")

        for effect in self.status_effects:
            if effect.get("name") == name:

                if stacking == "ignore":
                    return

                if stacking == "refresh":
                    effect["duration"] = duration
                    return

                if stacking == "overwrite":
                    effect["duration"] = duration
                    effect["data"] = dict(data)
                    return

                if stacking == "stack":
                    old_data = effect.setdefault("data", {})

                    old_amt = old_data.get("amount_per_turn", 0)
                    new_amt = data.get("amount_per_turn", 0)
                    old_data["amount_per_turn"] = old_amt + new_amt

                    old_data["flat"] = old_data.get("flat", 0) + data.get("flat", 0)
                    old_data["percent"] = old_data.get("percent", 0) + data.get("percent", 0)

                    effect["duration"] = max(effect.get("duration", 0), duration)
                    return

        self.status_effects.append({
            "name": name,
            "type": effect_type,
            "duration": duration,
            "data": dict(data)
        })


    def has_status(self, name):
        return any(e["name"] == name and e["duration"] > 0  for e in self.status_effects)
    

    def recalc_stats(self):
        self.attack = self.basic_attack
        self.defense = self.base_defense
        self.hit_chance = self.base_hit
        self.dodge_chance = self.base_dodge
        self.crit_chance = self.base_crit

        for effect in self.status_effects:
            definition=STATUS_DEFINITIONS[effect["name"]]
            if effect["type"] == "buff":
                stat = definition["stat"]
                flat = effect["data"].get("flat", 0)
                percent = effect["data"].get("percent", 0)
                setattr(self, stat, getattr(self, stat) * (1 + percent) + flat)
            elif effect["type"] == "debuff":
                stat = definition["stat"]
                percent = definition.get("percent", 0)
                setattr(self, stat, getattr(self, stat) * (1 + percent))
