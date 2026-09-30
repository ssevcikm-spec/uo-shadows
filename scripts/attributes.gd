extends Node

var Str := 10
var Dex := 10
var Int := 10

func hodnota(attr: String) -> int:
    match attr:
        "Str": return Str
        "Dex": return Dex
        "Int": return Int
        _: return 0

func derived() -> Dictionary:
    return {
        "damage": 1 + Str / 10,
        "hit_chance": 0.5 + Dex / 200,
        "attack_speed": 1.0 + Dex / 100,
        "mana": Int,
        "carry": 40 + Str,
    }
