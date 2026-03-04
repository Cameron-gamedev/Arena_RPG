# game/waves/wave_manager.py

from game.enemies.enemy_factory import EnemyFactory
from game.modifiers.modifier_engine import roll_modifiers, apply_modifiers, display_modifiers
from game.rewards.xp_system import calculate_wave_xp
from game.rewards.loot_generator import generate_wave_loot
from game.waves.wave_definitions import WAVE_DEFINITIONS


class WaveManager:
    def __init__(self, player, combat_engine_class):
        self.player = player
        self.combat_engine_class = combat_engine_class
        self.current_wave_index = 0

    def start_run(self):
        print("\n=== Arena Run Start ===")

        while self.current_wave_index < len(WAVE_DEFINITIONS):
            wave = WAVE_DEFINITIONS[self.current_wave_index]
            self.run_wave(wave)

            if self.player.is_dead():
                print("\nYou have fallen in the arena...")
                return

            self.current_wave_index += 1

        print("\n=== Victory! You cleared all waves! ===")

    def run_wave(self, wave):
        wave_number = wave["wave"]
        tier = wave["tier"]

        print(f"\n--- Wave {wave_number} ({tier.title()}) ---")

        # -------------------------
        # 1. Roll + apply modifiers
        # -------------------------
        random_mods = roll_modifiers(tier)
        forced_mods = wave.get("forced_modifiers", [])
        all_mods = random_mods + forced_mods

        display_modifiers(all_mods)

        # -------------------------
        # 2. Spawn enemies
        # -------------------------
        enemies = EnemyFactory.spawn_wave(
            wave["enemies"],
            wave_number,
            tier
        )

        # -------------------------
        # 3. Run combat
        # -------------------------
        engine = self.combat_engine_class(self.player, enemies)
        apply_modifiers(all_mods, engine, enemies, self.player)
        engine.start_combat()

        if self.player.is_dead():
            return

        # -------------------------
        # 4. XP Rewards
        # -------------------------
        xp = calculate_wave_xp(wave, enemies)
        print(f"\nYou gained {xp} XP!")
        self.player.gain_xp(xp)

        # -------------------------
        # 5. Loot Rewards
        # -------------------------
        is_boss_wave = any(e["boss"] for e in wave["enemies"])
        player_class = self.player.player_class_name

        loot = generate_wave_loot(
            wave["loot_table"],
            player_class,
            is_boss_wave=is_boss_wave
        )

        print("\nLoot Found:")
        for item in loot:
            added = self.player.inventory.add_item(item)
            status = "added to inventory" if added else "inventory full!"
            print(f" - {item.name} ({status})")

        # -------------------------
        # 6. Between-wave regen
        # -------------------------
        self.apply_between_wave_regen()

        # -------------------------
        # 7. Inventory management
        # -------------------------
        self.inventory_screen()

    # ---------------------------------------------------------
    # Between-wave regen (based on CLASS_DEFINITIONS)
    # ---------------------------------------------------------
    def apply_between_wave_regen(self):
        regen = self.player.player_class["between_wave_regen"]

        hp_gain = int(self.player.max_hp * regen["hp_percent"])
        mp_gain = int(self.player.max_mp * regen["mp_percent"])
        sp_gain = int(self.player.max_sp * regen["sp_percent"])

        self.player.current_hp = min(self.player.max_hp, self.player.current_hp + hp_gain)
        self.player.current_mp = min(self.player.max_mp, self.player.current_mp + mp_gain)
        self.player.current_sp = min(self.player.max_sp, self.player.current_sp + sp_gain)

        print("\n— Between-Wave Recovery —")
        print(f"HP +{hp_gain}, MP +{mp_gain}, SP +{sp_gain}")

    # ---------------------------------------------------------
    # Inventory management placeholder
    # ---------------------------------------------------------
    def inventory_screen(self):
        while True:
            print("\n=== Inventory Management ===")
            print("1. View Inventory")
            print("2. Equip Item")
            print("3. Unequip Item")
            print("4. Use Consumable")
            print("5. View Player Stats")
            print("6. Continue to Next Wave")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.show_inventory()

            elif choice == "2":
                self.equip_item_menu()

            elif choice == "3":
                self.unequip_item_menu()

            elif choice == "4":
                self.use_consumable_menu()

            elif choice == "5":
                self.show_player_stats()

            elif choice == "6":
                print("Preparing next wave...")
                return

            else:
                print("Invalid choice.")


    def show_inventory(self):
        print("\n--- Inventory ---")
        for i, item in enumerate(self.player.inventory.slots):
            if item:
                print(f"{i}: {item.name} (x{item.quantity})" if item.stackable else f"{i}: {item.name}")
            else:
                print(f"{i}: [Empty]")


    def equip_item_menu(self):
        self.show_inventory()
        slot = input("Enter inventory index to equip: ").strip()

        if not slot.isdigit():
            print("Invalid input.")
            return

        idx = int(slot)
        if idx < 0 or idx >= self.player.inventory.size:
            print("Invalid slot.")
            return

        item = self.player.inventory.slots[idx]
        if not item:
            print("No item in that slot.")
            return

        print("\nAvailable Equipment Slots:")
        for s in self.player.equipment.slots:
            print(f"- {s}")

        chosen_slot = input("Equip to which slot? ").strip()

        if chosen_slot not in self.player.equipment.slots:
            print("Invalid slot.")
            return

        if not self.player.equipment.can_equip(chosen_slot, item):
            print("Cannot equip that item in that slot.")
            return

        old_item = self.player.equipment.equip_item(chosen_slot, item)
        self.player.inventory.slots[idx] = None

        if old_item:
            self.player.inventory.add_item(old_item)

        self.player.recalculate_stats()
        print(f"Equipped {item.name} to {chosen_slot}.")


    def unequip_item_menu(self):
        print("\n--- Equipped Items ---")
        for slot, item in self.player.equipment.slots.items():
            print(f"{slot}: {item.name if item else '[Empty]'}")

        chosen_slot = input("Unequip which slot? ").strip()

        if chosen_slot not in self.player.equipment.slots:
            print("Invalid slot.")
            return

        removed = self.player.equipment.unequip_item(chosen_slot)
        if not removed:
            print("Slot already empty.")
            return

        added = self.player.inventory.add_item(removed)
        if not added:
            print("Inventory full! Item dropped.")
        else:
            print(f"Unequipped {removed.name}.")

        self.player.recalculate_stats()


    def use_consumable_menu(self):
        self.show_inventory()
        slot = input("Enter inventory index to use: ").strip()

        if not slot.isdigit():
            print("Invalid input.")
            return

        idx = int(slot)
        if idx < 0 or idx >= self.player.inventory.size:
            print("Invalid slot.")
            return

        item = self.player.inventory.slots[idx]
        if not item:
            print("No item in that slot.")
            return

        if not item.effect:
            print("That item is not a consumable.")
            return

        # Use the item via your existing system
        from game.combats.items import use_item
        use_item(self.player, self.player.inventory, idx)

        self.player.recalculate_stats()


    def show_player_stats(self):
        print("\n=== Player Stats ===")
        print(f"Level: {self.player.level}")
        print(f"HP: {self.player.current_hp}/{self.player.max_hp}")
        print(f"MP: {self.player.current_mp}/{self.player.max_mp}")
        print(f"SP: {self.player.current_sp}/{self.player.max_sp}")
        print(f"Attack: {self.player.attack}")
        print(f"Defense: {self.player.defense}")
        print(f"Crit Chance: {self.player.crit_chance:.2f}")
        print(f"Dodge Chance: {self.player.dodge_chance:.2f}")
        print(f"Hit Chance: {self.player.hit_chance:.2f}")
