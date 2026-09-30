extends Node

class_name Economy

var _gold: int = 0

func gold(player: Node) -> int:
    return _gold

func price(item: Node) -> int:
    var material_price: int = 0
    var quality_price: int = 0

    if item.material == "wood":
        material_price = 10
    elif item.material == "stone":
        material_price = 20
    elif item.material == "metal":
        material_price = 30

    if item.quality == "common":
        quality_price = 1
    elif item.quality == "uncommon":
        quality_price = 2
    elif item.quality == "rare":
        quality_price = 3
    elif item.quality == "epic":
        quality_price = 4
    elif item.quality == "legendary":
        quality_price = 5

    return material_price * quality_price

func buy(player: Node, item: Node) -> void:
    var item_price: int = price(item)

    if _gold >= item_price:
        _gold -= item_price
        player.add_item(item)
    else:
        push_error("Not enough gold to buy the item")

func sell(player: Node, item: Node) -> void:
    var item_price: int = price(item)

    _gold += item_price
    player.remove_item(item)
