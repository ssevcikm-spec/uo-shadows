func resolve(attacker, defender) -> Dictionary:
    # Calculate hit chance
    var hit_chance: float = 0.5
    # Dex from attributes
    if attacker.has_method("hodnota"):
        hit_chance += float(attacker.hodnota("Dex")) / 200.0
    # Skill "boj_na_blizko" from skills
    if attacker.has_method("hodnota"):
        hit_chance += float(attacker.hodnota("boj_na_blizko")) / 200.0

    var hit: bool = randf() < hit_chance
    var damage: int = 0

    if hit:
        # Base damage from Str attribute
        var base_damage: int = 1 + int(attacker.hodnota("Str") / 10)
        # Weapon damage if attacker has a weapon node with a `damage` property
        var weapon_damage: int = 0
        if attacker.has("zbran") and attacker.zbran != null:
            weapon_damage = int(attacker.zbran.damage)
        var total_damage: int = base_damage + weapon_damage

        # Defender armor rating (default 0)
        var armor: int = 0
        if defender.has("armor_rating"):
            armor = int(defender.armor_rating)
        damage = max(0, total_damage - armor)

    return {"hit": hit, "damage": damage}
