from game.combats.ui import player_choose_action
from game.combats.actions import player_attack
from game.combats.skills import player_choose_skill, use_skill
from game.combats.items import use_item
from game.combats.actions import enemy_use_action
from game.combats.status import process_status_effects, apply_passive_regen
from game.combats.ui import display_status


class CombatEngine:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies  # list of enemy objects
        self.round = 1
        self.combat_over = False

    # ============================================================
    # PLAYER TURN
    # ============================================================
    def run_player_turn(self):
        if not self.player.can_attack():
            print(f"{self.player.name} is stunned and cannot act this turn!")
            return

        while True:
            print("\nYour turn!")
            action = player_choose_action()

            # ------------------------------------------------------------
            # BASIC ATTACK
            # ------------------------------------------------------------
            if action == "attack":
                living = [e for e in self.enemies if not e.is_dead()]
                if not living:
                    print("No valid targets!")
                    continue

                for i, e in enumerate(living, start=1):
                    print(f"{i}. {e.name} {e.current_hp}/{e.max_hp} HP")

                choice = input("Target number: ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(living):
                        player_attack(self.player, living[idx])
                        break  # turn consumed

                print("Invalid choice.")
                continue

            # ------------------------------------------------------------
            # SKILLS
            # ------------------------------------------------------------
            elif action == "skills":
                chosen_skill = player_choose_skill(self.player)
                if not chosen_skill:
                    continue  # back to action menu

                from game.skills.skill_engine import execute_skill
                result = execute_skill(self.player, chosen_skill, self.enemies, allies=[self.player])

                if result == "cancel":
                    continue  # do not consume turn

                break  # skill succeeded → consume turn

            # ------------------------------------------------------------
            # ITEMS (combat consumables only)
            # ------------------------------------------------------------
            elif action == "items":
                used = self.use_combat_consumable_menu()
                if used:
                    break  # turn consumed
                else:
                    continue  # retry action menu
            elif action == "status":
                self.show_player_status_detailed()
                continue
            else:
                print("Invalid action.")
                continue

    # ============================================================
    # COMBAT ITEM MENU (CONSUMABLES ONLY)
    # ============================================================
    def use_combat_consumable_menu(self):
        print("\nChoose a consumable:")

        consumables = self.player.inventory.get_consumables()

        if not consumables:
            print("You have no consumables.")
            return False

        for i, (slot_index, item) in enumerate(consumables, start=1):
            print(f" {i}. {item.name} x{item.quantity}")

        print(" b. Back")

        choice = input("Item number: ").strip()

        if choice.lower() == "b":
            return False

        if not choice.isdigit():
            print("Invalid choice.")
            return False

        idx = int(choice) - 1
        if idx < 0 or idx >= len(consumables):
            print("Invalid choice.")
            return False

        slot_index, item = consumables[idx]

        used = use_item(self.player, self.player.inventory, slot_index)
        return used

    # ============================================================
    # ENEMY TURN
    # ============================================================
    def run_enemy_turn(self):
        print("\nEnemies' turn!")

        for enemy in [e for e in self.enemies if not e.is_dead()]:
            if not enemy.can_attack():
                print(f"{enemy.name} is stunned and skips its turn!")
                continue

            action = enemy.choose_action(self.player, self.enemies)
            enemy_use_action(enemy, self.player, action)

            if self.player.is_dead():
                break

    # ============================================================
    # END OF ROUND
    # ============================================================
    def end_round(self):
        process_status_effects(self.player)
        for enemy in self.enemies:
            if not enemy.is_dead():
                process_status_effects(enemy)

        apply_passive_regen(self.player)
        for enemy in self.enemies:
            if not enemy.is_dead():
                apply_passive_regen(enemy)

        # Tick skill cooldowns
        for skill_id in list(self.player.skill_cooldowns.keys()):
            self.player.skill_cooldowns[skill_id] -= 1
            if self.player.skill_cooldowns[skill_id] <= 0:
                del self.player.skill_cooldowns[skill_id]

        display_status(self.player, self.enemies)
        self.round += 1

    # ============================================================
    # START COMBAT (single wave only)
    # ============================================================
    def start_combat(self):
        print("\n=== Combat Start ===")
        from game.combats.ui import display_health
        display_health(self.player, self.enemies)

        while not self.combat_over and not self.player.is_dead():

            # PLAYER TURN
            self.run_player_turn()
            if self.player.is_dead():
                break

            # Check if wave is cleared
            if all(e.is_dead() for e in self.enemies):
                self.combat_over = True
                break

            # ENEMY TURN
            self.run_enemy_turn()
            if self.player.is_dead():
                break

            # END OF ROUND
            self.end_round()

        # COMBAT RESULT
        if self.player.is_dead():
            print("\nYou have fallen!")
        else:
            print("\nVictory!")

    
    def show_player_status_detailed(self):
        p = self.player

        print("\n=== Player Status ===")

        # -----------------------------
        # CORE RESOURCES
        # -----------------------------
        print(f"HP: {p.current_hp}/{p.max_hp}")
        print(f"MP: {p.current_mp}/{p.max_mp}")
        print(f"SP: {p.current_sp}/{p.max_sp}")

        # -----------------------------
        # FINAL COMBAT STATS
        # -----------------------------
        print("\n-- Combat Stats --")
        print(f"Attack:       {p.attack}")
        print(f"Defense:      {p.defense}")
        print(f"Crit Chance:  {p.crit_chance:.2f}")
        print(f"Dodge Chance: {p.dodge_chance:.2f}")
        print(f"Hit Chance:   {p.hit_chance:.2f}")

        # -----------------------------
        # ACTIVE STATUS EFFECTS
        # -----------------------------
        print("\n-- Active Effects --")

        if not p.status_effects:
            print("None")
        else:
            for effect in p.status_effects:
                name = effect["name"]
                duration = effect["duration"]
                data = effect.get("data", {})

                # Build readable modifier text
                mods = []
                if "flat" in data and data["flat"] != 0:
                    mods.append(f"flat {data['flat']:+}")
                if "percent" in data and data["percent"] != 0:
                    mods.append(f"{data['percent']*100:+.0f}%")

                if "amount_per_turn" in data:
                    mods.append(f"{data['amount_per_turn']} per turn")

                mod_text = ", ".join(mods) if mods else ""

                print(f"- {name} ({duration} turns) {mod_text}")

        # -----------------------------
        # REGEN EFFECTS (HOT)
        # -----------------------------
        if p.active_regen_effects:
            print("\n-- Regen Effects --")
            for r in p.active_regen_effects:
                print(f"- {r['target'].upper()} +{r['amount_per_turn']} ({r['turns_left']} turns)")

        # -----------------------------
        # COOLDOWNS
        # -----------------------------
        if p.skill_cooldowns:
            print("\n-- Cooldowns --")
            for skill_id, cd in p.skill_cooldowns.items():
                print(f"- {skill_id}: {cd} turns")

        print("\n==============================")
