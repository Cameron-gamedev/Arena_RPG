import random
from game.equipment import Equipment
from game.status.stat_modifiers import accumulate_status_modifiers
from game.status.status_definitions import STATUS_DEFINITIONS


class Player:
    def __init__(
        self,
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

        self.base_stats = {
            "strength": strength,
            "agility": agility,
            "vitality": vitality,
            "intelligence": intelligence
        }

        self.final_stats = {}

        # -----------------------------
        # BASE COMBAT STATS
        # -----------------------------
        self.base_atk = base_atk
        self.base_def = base_def

        # -----------------------------
        # INVENTORY & EQUIPMENT
        # -----------------------------
        from game.inventory import Inventory
        from game.slots.slot_definitions import SLOT_RULES

        self.inventory = Inventory(size=20)
        self.equipment = Equipment(SLOT_RULES)

        # -----------------------------
        # PROGRESSION
        # -----------------------------
        self.level = 1
        self.current_xp = 0

        # -----------------------------
        # RESOURCES
        # -----------------------------
        self.max_hp = 1
        self.current_hp = 1

        self.max_mp = 50
        self.current_mp = 50

        self.max_sp = 50
        self.current_sp = 50

        # Passive regen (class identity)
        self.passive_hp_regen = 0
        self.passive_mp_regen = 1
        self.passive_sp_regen = 2

        # -----------------------------
        # SKILLS & EFFECTS
        # -----------------------------
        self.skills = []
        self.skill_cooldowns = {}
        self.active_regen_effects = []   # HOT-like regen system
        self.status_effects = []         # Main buff/debuff/DOT/HOT system

        # -----------------------------
        # CLASS
        # -----------------------------
        self.player_class_name = None
        self.player_class = None
        self.class_passives = {}

        # Initial stat calculation
        self.recalculate_stats()

    def is_dead(self):
        return self.current_hp <= 0

    # ============================================================
    # CLASS SETUP
    # ============================================================
    def set_class(self, class_name):
        from game.classes.class_definitions import CLASS_DEFINITIONS

        self.player_class_name = class_name
        self.player_class = CLASS_DEFINITIONS[class_name]

        # Apply class base stats
        for stat, value in self.player_class["base_stats"].items():
            setattr(self, stat, value)
            self.base_stats[stat] = value

        # Apply class regen identity
        self.passive_hp_regen = self.player_class["regen"]["hp"]
        self.passive_mp_regen = self.player_class["regen"]["mp"]
        self.passive_sp_regen = self.player_class["regen"]["sp"]

        # Normalize class passives
        normalized = {}
        for key, val in self.player_class.get("passives", {}).items():
            if isinstance(val, (int, float)):
                normalized[key] = {"base": val, "scale": 0}
            else:
                normalized[key] = val
        self.class_passives = normalized

        # Load starting skills
        self.skills = []
        if 1 in self.player_class["skills"]:
            for skill_id in self.player_class["skills"][1]:
                self.skills.append(skill_id.lower())

        # Reset cooldowns
        self.skill_cooldowns = {}

        # Recalculate stats
        self.recalculate_stats()

        # Restore resources
        self.current_hp = self.max_hp
        self.current_mp = self.max_mp
        self.current_sp = self.max_sp

    # ============================================================
    # XP & LEVELING
    # ============================================================
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

        # Primary stat growth
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

        # Base ATK/DEF scaling
        if self.level % 2 == 0:
            self.base_atk += 1
        if self.level % 3 == 0:
            self.base_def += 1

        # Skill unlocks
        if self.level in self.player_class["skills"]:
            for skill_id in self.player_class["skills"][self.level]:
                self.skills.append(skill_id)

        # Heal on level-up
        self.current_hp = min(self.max_hp, self.current_hp + int(self.max_hp * 0.5))

        self.recalculate_stats()

    # ============================================================
    # STATUS & EFFECTS
    # ============================================================
    def apply_status(self, name, effect_type, duration, data=None):
        if data is None:
            data = {}

        definition = STATUS_DEFINITIONS.get(name)
        if definition is None:
            print(f"[Warning] Unknown status '{name}' attempted on {self.name}. Ignored.")
            return

        stacking = data.get("stacking", definition.get("stacking", "refresh"))

        # Check existing
        for effect in self.status_effects:
            if effect["name"] == name:

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
                    old_data["amount_per_turn"] = old_data.get("amount_per_turn", 0) + data.get("amount_per_turn", 0)
                    old_data["flat"] = old_data.get("flat", 0) + data.get("flat", 0)
                    old_data["percent"] = old_data.get("percent", 0) + data.get("percent", 0)
                    effect["duration"] = max(effect["duration"], duration)
                    return

        # Add new effect
        self.status_effects.append({
            "name": name,
            "type": effect_type,
            "duration": duration,
            "data": data
        })

        # Recalc immediately for buffs/debuffs
        if effect_type in ("buff", "debuff"):
            self.recalculate_stats()

    def has_status(self, name):
        return any(e["name"] == name and e["duration"] > 0 for e in self.status_effects)

    def clear_temporary_effects(self):
        """Remove all temporary combat effects at the end of a wave."""
        self.status_effects.clear()
        self.active_regen_effects.clear()
        self.skill_cooldowns.clear()

        self.recalculate_stats()
        print(f"\n-- All temporary effects cleared from {self.name}. --")

    # ============================================================
    # CORE STAT PIPELINE
    # ============================================================

    def recalculate_stats(self):
        # Preserve HP ratio
        hp_ratio = 1.0 if self.max_hp == 0 else self.current_hp / self.max_hp

        # ------------------------------------------------------------
        # STEP 1: Base + Equipment
        # ------------------------------------------------------------
        self.get_final_stats()

        # ------------------------------------------------------------
        # STEP 2: Apply status modifiers (buffs/debuffs)
        # ------------------------------------------------------------
        status_mods = accumulate_status_modifiers(self, self.final_stats)
        for stat, mod in status_mods.items():
            if stat not in self.final_stats:
                self.final_stats[stat] = {"base": 0, "flat": 0, "percent": 0, "final": None}
            self.final_stats[stat]["flat"] += mod["flat"]
            self.final_stats[stat]["percent"] += mod["percent"]

        # ------------------------------------------------------------
        # ⭐ STEP 3: RECOMPUTE PRIMARY STATS AFTER BUFFS/DEBUFFS
        # ------------------------------------------------------------
        for stat in ["strength", "agility", "vitality", "intelligence"]:
            base = self.final_stats[stat]["base"]
            flat = self.final_stats[stat]["flat"]
            percent = self.final_stats[stat]["percent"]
            self.final_stats[stat]["final"] = self.equipment._apply_percent_math(base, flat, percent)

        STR = self.final_stats["strength"]["final"]
        AGI = self.final_stats["agility"]["final"]
        VIT = self.final_stats["vitality"]["final"]
        INT = self.final_stats["intelligence"]["final"]

        # ------------------------------------------------------------
        # STEP 4: Equipment bonuses
        # ------------------------------------------------------------
        weapon_item = self.equipment.slots.get("weapon_main")
        weapon_bonus = weapon_item.attack_bonus if weapon_item else 0

        armor_item = self.equipment.slots.get("armor")
        armor_bonus = armor_item.defense_bonus if armor_item else 0

        accessory_bonus = 0
        for slot_name in ["ring_1", "ring_2", "amulet"]:
            item = self.equipment.slots.get(slot_name)
            if item and hasattr(item, "crit_bonus"):
                accessory_bonus += item.crit_bonus

        # ------------------------------------------------------------
        # STEP 5: Derived stats (now using UPDATED primary stats)
        # ------------------------------------------------------------
        self.max_hp = self._apply_derived_modifiers("max_hp", 50 + (VIT * 10))
        self.max_mp = 20 + (INT * 5)
        self.max_sp = 20 + (AGI * 3)

        self.attack = self._apply_derived_modifiers(
            "attack",
            (self.base_atk + weapon_bonus) + (STR * 1.5)
        )

        self.defense = self._apply_derived_modifiers(
            "defense",
            (self.base_def + armor_bonus) + (VIT * 0.5)
        )

        self.hit_chance = self._apply_derived_modifiers(
            "hit_chance",
            0.75 + (AGI * 0.002)
        )

        self.crit_chance = self._apply_derived_modifiers(
            "crit_chance",
            0.05 + (AGI * 0.003) + accessory_bonus
        )

        self.dodge_chance = self._apply_derived_modifiers(
            "dodge_chance",
            0.05 + (AGI * 0.004)
        )

        # Clamp
        self.hit_chance = min(self.hit_chance, 0.98)
        self.dodge_chance = min(self.dodge_chance, 0.60)
        self.crit_chance = min(self.crit_chance, 0.50)

        # ------------------------------------------------------------
        # STEP 6: Class passives
        # ------------------------------------------------------------
        for passive, values in self.class_passives.items():
            base = values.get("base", 0)
            scale = values.get("scale", 0)
            value = base + (self.level - 1) * scale

            if passive == "armor_bonus":
                self.defense += value
            elif passive == "crit_bonus":
                self.crit_chance += value
            elif passive == "dodge_bonus":
                self.dodge_chance += value
            elif passive == "spell_power_scaling":
                self.spell_power = INT * value
            elif passive == "healing_power":
                self.healing_power = value

        # ------------------------------------------------------------
        # STEP 7: Class resource identity
        # ------------------------------------------------------------
        if self.player_class_name == "Warrior":
            self.passive_sp_regen = 3
            self.passive_mp_regen = 0
        elif self.player_class_name == "Ranger":
            self.passive_sp_regen = 2
            self.passive_mp_regen = 0
        elif self.player_class_name == "Wizard":
            self.passive_sp_regen = 0
            self.passive_mp_regen = 4
        elif self.player_class_name == "Cleric":
            self.passive_sp_regen = 0
            self.passive_mp_regen = 3

        # ------------------------------------------------------------
        # STEP 8: Restore HP/MP/SP ratios
        # ------------------------------------------------------------
        self.current_hp = max(1, int(self.max_hp * hp_ratio))
        self.current_mp = min(self.current_mp, self.max_mp)
        self.current_sp = min(self.current_sp, self.max_sp)



    # ============================================================
    # UTILITY
    # ============================================================
    def get_final_stats(self):
        equipment_mods = self.equipment.get_total_modifiers(self.base_stats)

        breakdown = {}
        all_stats = set(self.base_stats) | set(equipment_mods["flat"]) | set(equipment_mods["percent"])

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

        # Derived stats placeholders
        for stat in ["attack", "defense", "crit_chance", "dodge_chance", "hit_chance", "max_hp"]:
            if stat in equipment_mods["flat"] or stat in equipment_mods["percent"]:
                breakdown[stat] = {
                    "base": 0,
                    "flat": equipment_mods["flat"].get(stat, 0),
                    "percent": equipment_mods["percent"].get(stat, 0),
                    "final": None
                }

        self.final_stats = breakdown
        return breakdown

    def _apply_derived_modifiers(self, stat_name, base_value):
        flat = self.final_stats.get(stat_name, {}).get("flat", 0)
        percent = self.final_stats.get(stat_name, {}).get("percent", 0)
        return (base_value + flat) * (1 + percent)

    # ============================================================
    # COMBAT
    # ============================================================
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
