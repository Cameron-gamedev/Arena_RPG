
def calculate_enemy_xp(enemy, wave_number):
    base = 20

    if enemy.is_boss:
        base *= 4
    elif enemy.is_elite:
        base *= 2

    return int(base * (1 + wave_number * 0.10))


def calculate_wave_xp(wave_config, enemies):
    total = 0
    wave_number = wave_config["wave"]
    multiplier = wave_config.get("xp_multiplier", 1.0)

    for e in enemies:
        total += calculate_enemy_xp(e, wave_number)

    return int(total * multiplier)
