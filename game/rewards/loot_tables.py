LOOT_TABLES = {
    "early": {
        "common": ["minor_health_potion", "wooden_shield", "simple_ring"],
        "uncommon": ["iron_sword", "leather_armor"],
        "rare": ["belt_of_strength"],
        "epic": [],
        "class_specific": {
            "Warrior": ["iron_sword", "wooden_shield"],
            "Wizard": ["basic_amulet"],
            "Ranger": ["simple_ring"],
            "Cleric": ["rejuvenation_potion"]
        }
    },

    "midgame": {
        "common": ["minor_health_potion", "rejuvenation_potion"],
        "uncommon": ["iron_sword", "leather_armor", "wooden_shield"],
        "rare": ["warriors_charm", "champions_gauntlets"],
        "epic": [],
        "class_specific": {
            "Warrior": ["champions_gauntlets"],
            "Wizard": ["basic_amulet"],
            "Ranger": ["warriors_charm"],
            "Cleric": ["rejuvenation_potion"]
        }
    },

    "boss": {
        "common": [],
        "uncommon": ["champions_gauntlets"],
        "rare": ["belt_of_strength", "warriors_charm"],
        "epic": ["basic_amulet"],
        "class_specific": {
            "Warrior": ["champions_gauntlets"],
            "Wizard": ["basic_amulet"],
            "Ranger": ["warriors_charm"],
            "Cleric": ["basic_amulet"]
        }
    },

    "final_boss": {
        "common": [],
        "uncommon": [],
        "rare": ["champions_gauntlets"],
        "epic": ["basic_amulet", "warriors_charm"],
        "class_specific": {
            "Warrior": ["champions_gauntlets"],
            "Wizard": ["basic_amulet"],
            "Ranger": ["warriors_charm"],
            "Cleric": ["basic_amulet"]
        }
    }
}
