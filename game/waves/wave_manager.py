
from game.enemies.enemy_factory import EnemyFactory
from game.modifiers.modifier_engine import roll_modifiers, apply_modifiers, display_modifiers
from game.rewards.xp_system import calculate_wave_xp
from game.rewards.loot_generator import generate_wave_loot
from game.waves.wave_definitions import WAVE_DEFINITIONS
from game.save_system import save_run_state


class WaveManager:
    def __init__(self, player, combat_engine_class, current_wave_index=0):
        self.player = player
        self.combat_engine_class = combat_engine_class
        self.current_wave_index = current_wave_index


    def start_run(self):
        print("\n=== Arena Run Start ===")

        while self.current_wave_index < len(WAVE_DEFINITIONS):
            wave = WAVE_DEFINITIONS[self.current_wave_index]
            self.run_wave(wave)

            if self.player.is_dead():
                print("\nYou have fallen in the arena...")
                return

            self.current_wave_index += 1
            self.save_checkpoint(save_type="checkpoint")

        print("\n=== Victory! You cleared all waves! ===")


    def save_checkpoint(self, save_type="checkpoint"):
        save_run_state(self.player, self.current_wave_index, save_type=save_type)
        print(f"[Save] {save_type.title()} saved for wave {self.current_wave_index + 1}.")


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
        self.player.clear_temporary_effects()

        self.apply_between_wave_regen()

        # -------------------------
        # 7. Inventory management
        # -------------------------
        self.inventory_screen()


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

   
    def inventory_screen(self):
        while True:
            print("\n=== Inventory Management ===")
            print("1. View Inventory")
            print("2. Equip Item")
            print("3. Unequip Item")
            print("4. Use Consumable")
            print("5. View Player Stats")
            print("6. Continue to Next Wave")
            print("7. Drop Item")
            print("8. View Equipped Items")
            print("9. Save and Quit")

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

            elif choice == "7":
                self.drop_item_menu()

            elif choice == "8":
                self.show_equipped_items()

            elif choice == "9":
                self.save_checkpoint(save_type="quick")
                print("Run saved. Exiting game.")
                raise SystemExit

            else:
                print("Invalid choice.")


    def show_inventory(self):
        print("\n--- Inventory ---")
        for i, item in enumerate(self.player.inventory.slots):
            if item:
                print(f"{i}: {item.name} (x{item.quantity})" if item.stackable else f"{i}: {item.name}")
            else:
                print(f"{i}: [Empty]")


    def show_equipped_items(self):
        print("\n=== Equipped Items ===")

        equipment = self.player.equipment.slots

        # If no equipment at all
        if all(item is None for item in equipment.values()):
            print("No items equipped.")
            return

        for slot_name, item in equipment.items():
            if item is None:
                print(f"{slot_name}: (empty)")
            else:
                print(f"{slot_name}: {item.name}")


    def equip_item_menu(self):
        print("\n=== Equip Item ===")

        equipment_items = self.player.inventory.get_equipment()

        if not equipment_items:
            print("You have no equipment items.")
            return False

        # Display equipment items
        for i, (slot_index, item) in enumerate(equipment_items, start=1):
            print(f" {i}. {item.name}")

        print(" b. Back")

        choice = input("Choose an item to equip: ").strip()

        if choice.lower() == "b":
            return False

        if not choice.isdigit():
            print("Invalid choice.")
            return False

        idx = int(choice) - 1
        if idx < 0 or idx >= len(equipment_items):
            print("Invalid choice.")
            return False

        slot_index, item = equipment_items[idx]

        # Determine valid slots for this item
        valid_slots = []
        for slot_name, rule in self.player.equipment.slot_rules.items():
            if item.item_type in rule["allowed_types"]:
                valid_slots.append(slot_name)

        if not valid_slots:
            print(f"{item.name} cannot be equipped.")
            return False

        # If only one valid slot, equip automatically
        if len(valid_slots) == 1:
            slot_name = valid_slots[0]
        else:
            print("\nChoose a slot:")
            for i, slot_name in enumerate(valid_slots, start=1):
                print(f" {i}. {slot_name.replace('_', ' ').title()}")

            slot_choice = input("Slot number: ").strip()
            if not slot_choice.isdigit():
                print("Invalid choice.")
                return False

            sidx = int(slot_choice) - 1
            if sidx < 0 or sidx >= len(valid_slots):
                print("Invalid choice.")
                return False

            slot_name = valid_slots[sidx]

        # Equip using your Equipment class
        old_item = self.player.equipment.equip_item(slot_name, item)

        # Remove from inventory
        self.player.inventory.remove_item(slot_index)

        # Return old item to inventory if needed
        if old_item:
            self.player.inventory.add_item(old_item)

        print(f"{item.name} equipped in {slot_name.replace('_', ' ').title()}.")
        return True


    def unequip_item_menu(self):
        print("\n=== Unequip Item ===")

        equipped_items = [
            (slot_name, item)
            for slot_name, item in self.player.equipment.slots.items()
            if item is not None
        ]

        if not equipped_items:
            print("No items are currently equipped.")
            return False

        for i, (slot_name, item) in enumerate(equipped_items, start=1):
            print(f" {i}. {item.name} ({slot_name.replace('_', ' ').title()})")

        print(" b. Back")

        choice = input("Choose an item to unequip: ").strip()

        if choice.lower() == "b":
            return False

        if not choice.isdigit():
            print("Invalid choice.")
            return False

        idx = int(choice) - 1
        if idx < 0 or idx >= len(equipped_items):
            print("Invalid choice.")
            return False

        slot_name, item = equipped_items[idx]

        removed = self.player.equipment.unequip_item(slot_name)

        if removed:
            self.player.inventory.add_item(removed)
            print(f"{item.name} unequipped.")
            return True

        print("Could not unequip item.")
        return False


    def use_consumable_menu(self):
        print("\nChoose a consumable:")

        # Use the new helper — this is the key fix
        consumables = self.player.inventory.get_consumables()

        if not consumables:
            print("You have no consumables.")
            return False

        # Display consumables only
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

        # Use the updated use_item() with index
        from game.combats.items import use_item
        used = use_item(self.player, self.player.inventory, slot_index)

        return used


    def drop_item_menu(self):
        print("\n=== Drop Item ===")

        all_items = self.player.inventory.get_all_items()

        if not all_items:
            print("Your inventory is empty.")
            return False

        # Display items
        for i, (slot_index, item) in enumerate(all_items, start=1):
            qty = f"x{item.quantity}" if item.stackable else ""
            print(f" {i}. {item.name} {qty}")

        print(" b. Back")

        choice = input("Choose an item to drop: ").strip()

        if choice.lower() == "b":
            return False

        if not choice.isdigit():
            print("Invalid choice.")
            return False

        idx = int(choice) - 1
        if idx < 0 or idx >= len(all_items):
            print("Invalid choice.")
            return False

        slot_index, item = all_items[idx]

        # ------------------------------------------------------------
        # NON‑STACKABLE ITEMS
        # ------------------------------------------------------------
        if not item.stackable:
            confirm = input(f"Drop {item.name}? (y/n): ").strip().lower()
            if confirm != "y":
                print("Canceled.")
                return False

            removed = self.player.inventory.remove_item(slot_index)
            if removed:
                print(f"{removed.name} dropped.")
                return True

            print("Could not drop item.")
            return False

        # ------------------------------------------------------------
        # STACKABLE ITEMS — QUANTITY PROMPT
        # ------------------------------------------------------------
        print(f"\n{item.name} x{item.quantity}")
        print("1. Drop 1")
        print("2. Drop custom amount")
        print("3. Drop entire stack")
        print("b. Back")

        q_choice = input("Choose an option: ").strip()

        if q_choice.lower() == "b":
            return False

        # Drop 1
        if q_choice == "1":
            item.quantity -= 1
            if item.quantity <= 0:
                self.player.inventory.remove_item(slot_index)
            print(f"Dropped 1 {item.name}.")
            return True

        # Drop custom amount
        elif q_choice == "2":
            amount = input("How many to drop? ").strip()
            if not amount.isdigit():
                print("Invalid amount.")
                return False

            amount = int(amount)
            if amount <= 0 or amount > item.quantity:
                print("Invalid amount.")
                return False

            item.quantity -= amount
            if item.quantity <= 0:
                self.player.inventory.remove_item(slot_index)

            print(f"Dropped {amount} {item.name}.")
            return True

        # Drop entire stack
        elif q_choice == "3":
            confirm = input(f"Drop ALL {item.quantity} {item.name}? (y/n): ").strip().lower()
            if confirm != "y":
                print("Canceled.")
                return False

            self.player.inventory.remove_item(slot_index)
            print(f"Dropped all {item.name}.")
            return True

        print("Invalid choice.")
        return False

  
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
