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



    def run_player_turn(self):
        if not self.player.can_attack():
            print(f"{self.player.name} is stunned and cannot act this turn!")
            return

        print("\nYour turn!")
        action = player_choose_action()

        if action == "attack":
            living = [e for e in self.enemies if not e.is_dead()]
            for i, e in enumerate(living, start=1):
                print(f"{i}. {e.name} {e.current_hp}/{e.max_hp} HP")

            choice = input("Target number: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(living):
                    player_attack(self.player, living[idx])

        elif action == "skills":
            chosen_skill = player_choose_skill(self.player)
            if chosen_skill:
                use_skill(self.player, chosen_skill, self.enemies)

        elif action == "items":
            use_item(self.player, self.player.inventory)

        # Cooldowns
        for skill_id in list(self.player.skill_cooldowns.keys()):
            self.player.skill_cooldowns[skill_id] -= 1
            if self.player.skill_cooldowns[skill_id] <= 0:
                del self.player.skill_cooldowns[skill_id]


    def run_enemy_turn(self):

        for e in self.enemies:
            print(e.name, type(e.is_dead))

        print("\nEnemies' turn!")
        for enemy in [e for e in self.enemies if not e.is_dead()]:
            if enemy.can_attack():
                action = enemy.choose_action(self.player, self.enemies)
                enemy_use_action(enemy, self.player, action)
            else:
                print(f"{enemy.name} is stunned and skips its turn!")

            if self.player.is_dead():
                break


    def end_round(self):
        process_status_effects(self.player)
        for enemy in self.enemies:
            if not enemy.is_dead():
                process_status_effects(enemy)
        
        apply_passive_regen(self.player)
        for enemy in self.enemies:
            if not enemy.is_dead():
                apply_passive_regen(enemy)


        display_status(self.player, self.enemies)
        self.round += 1


    def check_wave_completion(self):
        if all(e.is_dead() for e in self.enemies):
            self.current_wave += 1
            if self.current_wave >= len(self.waves):
                self.combat_over = True
                return

            print(f"\n--- Wave {self.current_wave + 1} begins! ---")
            self.enemies = self.waves[self.current_wave]


    def start_combat(self):
        print("\n=== Combat Start ===")
        from game.combats.ui import display_health
        display_health(self.player, self.enemies)

        while not self.combat_over and not self.player.is_dead():

            self.run_player_turn()
            if self.player.is_dead():
                break

            # Check if all enemies are dead
            if all(e.is_dead() for e in self.enemies):
                self.combat_over = True
                break

            self.run_enemy_turn()
            if self.player.is_dead():
                break

            self.end_round()

        if self.player.is_dead():
            print("\nYou have fallen!")
        else:
            print("\nVictory!")
