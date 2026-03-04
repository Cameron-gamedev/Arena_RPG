from game.enemies.enemy import Enemy
import random

class OrcWarcaller(Enemy):
    def __init__(self, level):
        name = "Orc Warcaller"
        max_hp = 48
        attack = 9
        defense = 6

        super().__init__(name, level, max_hp, attack, defense)

        self.hit_chance = 0.80
        self.dodge_chance = 0.05
        self.crit_chance = 0.10
        self.armor_defense = 1

        self.base_attack = attack
        self.base_defense = defense
        self.base_hit = self.hit_chance
        self.base_dodge = self.dodge_chance
        self.base_crit = self.crit_chance

        self.passive_hp_regen = 0
        self.passive_mp_regen = 0
        self.passive_sp_regen = 2

        self.warcry_cd = 0
        self.drums_cd = 0
        self.chant_cd = 0

        self.warcry = {"name": "Warcry", "skip": True}
        self.drums_of_battle = {"name": "Drums of Battle", "skip": True}

        self.battle_chant = {
            "name": "Battle Chant",
            "damage": {"flat": 0, "scaling": {}, "hits": 0},
            "status_effects": [{"name": "Weaken", "duration": 2}]
        }

        self.basic_attack = {
            "name": "Warcaller Strike",
            "damage": {"flat": 3, "scaling": {"attack": 0.40}, "hits": 1},
            "status_effects": []
        }

    def choose_action(self, player, allies=None):
        if allies is None:
            allies = []

        if self.warcry_cd > 0: self.warcry_cd -= 1
        if self.drums_cd > 0: self.drums_cd -= 1
        if self.chant_cd > 0: self.chant_cd -= 1

        if self.warcry_cd == 0:
            for ally in allies:
                if not ally.is_dead() and not ally.has_status("Warcry"):
                    print(f"{self.name} bellows a mighty Warcry!")
                    self.warcry_cd = 3
                    for a in allies:
                        if not a.is_dead():
                            a.apply_status("Warcry", "buff", 2, {"percent": 0.15})
                    return self.warcry

        if self.drums_cd == 0:
            low_sp = [a for a in allies if not a.is_dead() and a.current_sp < a.max_sp * 0.40]
            if low_sp:
                print(f"{self.name} beats the Drums of Battle!")
                self.drums_cd = 4
                for a in allies:
                    if not a.is_dead():
                        a.apply_status("DrumsOfBattle", "buff", 2, {"flat": 1})
                return self.drums_of_battle

        living = [a for a in allies if not a.is_dead()]
        if len(living) == 1:
            if self.chant_cd == 0:
                self.chant_cd = 3
                return self.battle_chant
            return self.basic_attack

        if self.chant_cd == 0 and random.random() < 0.30:
            self.chant_cd = 3
            return self.battle_chant

        return self.basic_attack
