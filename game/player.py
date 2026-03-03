import random
from game.equipment import Equipment  
from game.status.stat_modifiers import accumulate_status_modifiers
from game.status.status_definitions import STATUS_DEFINITIONS


class Player:
    def __init__(self, 
            name, 
            strength, 
            agility, 
            vitality, 
            intelligence,
            base_atk,
            base_def,
        ):

        # -----------------------------
        # PRIMARY STATS (permanent)
        # -----------------------------
        self.name = name
        self.strength = strength
        self.agility = agility
        self.vitality = vitality
        self.intelligence = intelligence

        # Dictionary version of base stats
        self.base_stats = {
            "strength": self.strength,
            "agility": self.agility,
            "vitality": self.vitality,
            "intelligence": self.intelligence
        }

        # Computed stats
        self.final_stats = {}

        # -----------------------------
        # BASE COMBAT STATS
        # -----------------------------
        self.base_atk = base_atk
        self.base_def = base_def
        
        # -----------------------------
        # Player Inventory
        # -----------------------------
        from game.inventory import Inventory
        self.inventory = Inventory(size=20)

        # -----------------------------
        # EQUIPMENT SYSTEM
        # -----------------------------
        from game.slots.slot_definitions import SLOT_RULES
        self.equipment = Equipment(SLOT_RULES)

        # -----------------------------
        # PROGRESSION
        # -----------------------------
        self.level = 1
        self.current_xp = 0
        self.xp_to_level = 100

        # -----------------------------
        # HP
        # -----------------------------
        self.max_hp = 1
        self.current_hp = 1

        # -----------------------------
        # RESOURCES
        # -----------------------------
        self.max_mp = 50
        self.current_mp = 50

        self.max_sp = 50
        self.current_sp = 50

        self.passive_hp_regen = 0
        self.passive_mp_regen = 1
        self.passive_sp_regen = 2

        # -----------------------------
        # SKILL & COOLDOWNS
        # -----------------------------
        self.skills=[]
        self.skill_cooldowns = {}  # skill_id → turns remaining
        
        # -----------------------------
        # Active Effects & Buffs
        # -----------------------------
        self.active_regen_effects = []
        self.active_buffs = []
        self.status_effects = []

        # -----------------------------
        # Set Player Class
        # -----------------------------
        self.player_class_name = None
        self.player_class = None

        # Initial stat calculation
        self.recalculate_stats()


    def set_class(self, class_name):
        from game.classes.class_definitions import CLASS_DEFINITIONS
        self.player_class_name = class_name
        self.player_class = CLASS_DEFINITIONS[class_name]

        # Apply base stats
        for stat, value in self.player_class["base_stats"].items():
            setattr(self, stat, value)
            self.base_stats[stat] = value

        # Apply regen
        self.passive_hp_regen = self.player_class["regen"]["hp"]
        self.passive_mp_regen = self.player_class["regen"]["mp"]
        self.passive_sp_regen = self.player_class["regen"]["sp"]

        self.class_passives = self.player_class.get("passives", {})

        self.recalculate_stats()


    def is_dead(self):
        return self.current_hp <= 0

    
    def xp_required_for_next_level(self):
        base_xp = 100
        return int(base_xp * (self.level ** 1.5))

    
    def gain_xp(self, amount):
        self.current_xp += amount

        while self.current_xp >= self.xp_required_for_next_level():
            self.current_xp -= self.xp_required_for_next_level()
            self.level_up()

   
    def level_up(self):
        self.level += 1
        growth = self.player_class["growth"]

        self.strength += growth["strength"]
        self.agility += growth["agility"]
        self.vitality += growth["vitality"]
        self.intelligence += growth["intelligence"]

        # Sync base_stats
        self.base_stats["strength"] = self.strength
        self.base_stats["agility"] = self.agility
        self.base_stats["vitality"] = self.vitality
        self.base_stats["intelligence"] = self.intelligence

        # Resource scaling
        res = self.player_class["resources"]
        self.max_hp += res["hp_per_level"]
        self.max_mp += res["mp_per_level"]
        self.max_sp += res["sp_per_level"]

        # Skill unlocks
        if self.level in self.player_class["skills"]:
            for skill_id in self.player_class["skills"][self.level]:
                self.skills.append(skill_id)

        self.current_hp = min(self.max_hp, self.current_hp + int(self.max_hp * 0.5))


        self.recalculate_stats()

    
    def get_final_stats(self):
        """
        Computes final stats using:
        - base stats
        - flat modifiers
        - percent modifiers
        Stores results in self.final_stats
        """

        equipment_mods = self.equipment.get_total_modifiers(self.base_stats)

        breakdown = {}

        all_stats = set(self.base_stats) \
                    | set(equipment_mods["flat"]) \
                    | set(equipment_mods["percent"])

        for stat in all_stats:
            base = self.base_stats.get(stat, 0)
            flat = equipment_mods["flat"].get(stat, 0)
            percent = equipment_mods["percent"].get(stat, 0)

            final_value = self.equipment._apply_percent_math(base, flat, percent)

            breakdown[stat] = {
                "base": base,
                "flat": flat,
                "percent": percent,
                "final": final_value
            }
        derived_stats = ["attack", "defense", "crit_chance", "dodge_chance", "hit_chance", "max_hp"]

        for stat in derived_stats:
            if stat in equipment_mods["flat"] or stat in equipment_mods["percent"]:
                flat = equipment_mods["flat"].get(stat, 0)
                percent = equipment_mods["percent"].get(stat, 0)

                breakdown[stat] = {
                    "base":0, # derived stats don't have base values here
                    "flat":flat,
                    "percent":percent,
                    "final": None # filled in during recalc
                }

        self.final_stats = breakdown
        print("DEBUG equipment_mods:", equipment_mods)

        return breakdown
    
   
    def _apply_derived_modifiers(self, stat_name, base_value):
        """
        Applies flat and percent modifiers to a derived stat.
        (base + flat) * (1 + percent)
        """
        flat = self.final_stats.get(stat_name, {}).get("flat",0)
        percent = self.final_stats.get(stat_name, {}).get("percent", 0)
        return (base_value + flat) * (1 + percent)
    

    def apply_status(self, name, effect_type, duration, data=None):
        from game.status.status_definitions import STATUS_DEFINITIONS

        if data is None:
            data = {}

        definition = STATUS_DEFINITIONS.get(name)
        
        if definition is None:
            print(f"[Warning] Unknown status '{name}' attempted on {self.name}. Ignored.")
            return
        
        stacking = data.get("stacking", definition.get("stacking", "refresh"))

        # Check if effect already exists
        for effect in self.status_effects:
            if effect["name"] == name:
                # --- STACKING RULES ---
                if stacking == "ignore":
                    return

                if stacking == "refresh":
                    effect["duration"] = duration
                    return

                if stacking == "overwrite":
                    effect["duration"] = duration
                    effect["data"] = data
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
                
        # If no existing effect, add new
        self.status_effects.append({
            "name": name,
            "type": effect_type,
            "duration": duration,
            "data": data
        })
    

    def has_status(self, name):
        return any(e["name"] == name and e["duration"] > 0 for e in self.status_effects)


    def recalculate_stats(self):
        # --- 1. Preserve HP ratio ---
        hp_ratio = 1.0 if self.max_hp == 0 else self.current_hp / self.max_hp

        # --- 2. Compute final primary stats ---
        self.get_final_stats()

        # --- Apply unified buff effects ---
        status_mods = accumulate_status_modifiers(self, self.final_stats)

        # Apply modifiers to final_stats
        for stat, mod in status_mods.items():
            if stat not in self.final_stats:
                self.final_stats[stat] = {"base": 0, "flat": 0, "percent": 0, "final": None}

            self.final_stats[stat]["flat"] += mod["flat"]
            self.final_stats[stat]["percent"] += mod["percent"]

        STR = self.final_stats["strength"]["final"]
        AGI = self.final_stats["agility"]["final"]
        VIT = self.final_stats["vitality"]["final"]
        INT = self.final_stats["intelligence"]["final"]    
        
        weapon_item = self.equipment.slots.get("weapon_main")
        weapon_bonus = weapon_item.attack_bonus if weapon_item else 0 

        armor_item = self.equipment.slots.get("armor")
        armor_bonus = armor_item.defense_bonus if armor_item else 0

        # --- Accessory crit bonus (supports multiple accessories) ---
        accessory_bonus = 0
        for slot_name in ["ring_1", "ring_2", "amulet"]:
            item = self.equipment.slots.get(slot_name)
            if item and hasattr(item, "crit_bonus"):
                accessory_bonus += item.crit_bonus

        # --- 3. Recalculate Resources ---
        self.max_hp = 100 + (VIT * 15)
        self.max_hp = self._apply_derived_modifiers("max_hp", self.max_hp)
        
        self.max_mp = int(20 + int(INT * 5))
        self.current_mp = min(self.current_mp, self.max_mp)

        self.max_sp = int(20 + int(INT * 5))
        self.current_sp = min(self.current_sp, self.max_sp)

        # --- 4. Derived Stats (using final stats) ---
        self.attack = (self.base_atk + weapon_bonus) * (1 + STR * 0.03)
        self.attack = self._apply_derived_modifiers("attack", self.attack)

        self.hit_chance = 0.75 + (AGI * 0.002)
        self.hit_chance = self._apply_derived_modifiers("hit_chance", self.hit_chance)

        self.defense = self.base_def + armor_bonus
        self.defense = self._apply_derived_modifiers("defense", self.defense)

        self.crit_chance = 0.10 + (AGI * 0.004) + accessory_bonus
        self.crit_chance = self._apply_derived_modifiers("crit_chance", self.crit_chance)

        self.dodge_chance = 0.50 +(AGI * 0.002)
        self.dodge_chance = self._apply_derived_modifiers("dodge_chance", self.dodge_chance)

        # --- Apply class passives (linear scaling) ---
        for passive, values in self.class_passives.items():
            base = values.get("base", 0)
            scale = values.get("scale", 0)
            value = base + (self.level - 1) * scale

            if passive == "armor_bonus":
                self.final_stats.setdefault("defense", {"base":0,"flat":0,"percent":0,"final":None})
                self.final_stats["defense"]["flat"] += value

            elif passive == "crit_bonus":
                self.final_stats.setdefault("crit_chance", {"base":0,"flat":0,"percent":0,"final":None})
                self.final_stats["crit_chance"]["flat"] += value

            elif passive == "dodge_bonus":
                self.final_stats.setdefault("dodge_chance", {"base":0,"flat":0,"percent":0,"final":None})
                self.final_stats["dodge_chance"]["flat"] += value

            elif passive == "spell_power_scaling":
                self.spell_power = INT * value

            elif passive == "healing_power":
                self.healing_power = value


        # --- 5. Restore HP ratio ---
        self.current_hp = max(1, int(self.max_hp * hp_ratio))


    def add_regen_effect(self, target, total_amount, duration):
        amount_per_turn = max(1, total_amount // duration)

        self.active_regen_effects.append({
            "target": target,
            "amount_per_turn": amount_per_turn,
            "turns_left": duration
        })


    def can_attack(self):
        for effect in self.status_effects:
            if effect["type"] == "stun" and effect["duration"] > 0:
                return False
        return True


    def take_damage(self, attacker, amount, source=None):
        amount = max(0, int(amount))

        before = self.current_hp
        self.current_hp = max(0, self.current_hp - amount)

        src_text = f" with {source}" if source else ""
        attacker_name = attacker.name if attacker is not None else "Unknown"
        print(f"{attacker_name} hits {self.name}{src_text} for {amount} damage! "
              f"({before} → {self.current_hp})")
