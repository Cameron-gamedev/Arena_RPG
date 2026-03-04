from game.status.status_definitions import STATUS_DEFINITIONS
from game.status.stat_modifiers import accumulate_status_modifiers

class Enemy:
    def __init__(self, name, level, max_hp, attack, defense):
        self.name = name
        self.level = level
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

        self.is_boss = False
        self.is_elite = False


        self.status_effects = []

    
    def choose_action(self, player, allies=None):
        raise NotImplementedError(f"{self.name} has no AI defined.")

    
    def take_damage(self, attacker, amount, source=None):
        amount = max(0, int(amount))

        before = self.current_hp
        self.current_hp = max(0, self.current_hp - amount)

        src_text = f" with {source}" if source else ""
        attacker_name = attacker.name if attacker is not None else "Unknown"
        print(f"{attacker_name} hits {self.name}{src_text} for {amount} damage! "
              f"({before} → {self.current_hp})")


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

        stacking = data.get("stacking", definition.get("stacking", "refresh"))

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
        # Reset to base
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.hit_chance = self.base_hit
        self.dodge_chance = self.base_dodge
        self.crit_chance = self.base_crit
        self.armor_defense = getattr(self, "armor_defense", 0)

        # Collect modifiers
        status_mods = accumulate_status_modifiers(self, {})

        # Apply modifiers
        for stat, mod in status_mods.items():
            if hasattr(self, stat):
                base_value = getattr(self, stat)
                new_value = (base_value + mod["flat"]) * (1 + mod["percent"])
                setattr(self, stat, new_value)
