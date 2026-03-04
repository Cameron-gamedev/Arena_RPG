
def apply_orc_fury(engine, enemies, player):
    for e in enemies:
        if not e.is_dead():
            e.apply_status("AttackUp", "buff", duration=999, data={"percent": 0.15})

def apply_burning_ground(engine, enemies, player):
    player.apply_status("Burn", "dot", duration=999, data={"amount_per_turn": 4})

def apply_spirit_drain(engine, enemies, player):
    player.apply_status("SpiritDrain", "debuff", duration=999, data={"mp_loss": 2, "sp_loss": 2})

def apply_regeneration_aura(engine, enemies, player):
    for e in enemies:
        if not e.is_dead():
            e.apply_status("Regen", "hot", duration=999, data={"percent": 0.03})

def apply_quickfooted(engine, enemies, player):
    for e in enemies:
        e.apply_status("DodgeUp", "buff", duration=999, data={"percent": 0.05})

def apply_sharpened_blades(engine, enemies, player):
    for e in enemies:
        e.apply_status("HitUp", "buff", duration=999, data={"percent": 0.10})

def apply_battlefield_smoke(engine, enemies, player):
    player.apply_status("HitDown", "debuff", duration=999, data={"percent": -0.10})


MODIFIER_DEFINITIONS = {
    "OrcFury": {
        "description": "Enemies gain +15% attack.",
        "apply": apply_orc_fury
    },
    "BurningGround": {
        "description": "Player takes 4 Burn damage per turn.",
        "apply": apply_burning_ground
    },
    "SpiritDrain": {
        "description": "Player loses 2 MP and 2 SP per turn.",
        "apply": apply_spirit_drain
    },
    "RegenerationAura": {
        "description": "Enemies regenerate 3% HP per turn.",
        "apply": apply_regeneration_aura
    },
    "Quickfooted": {
        "description": "Enemies gain +5% dodge chance.",
        "apply": apply_quickfooted
    },
    "SharpenedBlades": {
        "description": "Enemies gain +10% hit chance.",
        "apply": apply_sharpened_blades
    },
    "BattlefieldSmoke": {
        "description": "Player hit chance reduced by 10%.",
        "apply": apply_battlefield_smoke
    }
}
