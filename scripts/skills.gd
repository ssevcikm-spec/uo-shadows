extends Node

var dovednosti: Dictionary = {
    "tezba": 0,
    "drevorubectvi": 0,
    "kovarstvi": 0,
    "boj_na_blizko": 0
}

func add(skill: String, n: int) -> void:
    dovednosti[skill] = clamp(dovednosti[skill] + n, 0, 100)

func hodnota(skill: String) -> int:
    return dovednosti[skill]
