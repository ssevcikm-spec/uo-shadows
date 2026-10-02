extends Node

var rules := []

func add_rule(trigger: String, action: String) -> void:
    rules.append({"trigger": trigger, "action": action})

func evaluate(player: Node) -> Array:
    var actions := []
    for rule in rules:
        if rule.trigger == "hp < X" and player.hp < player.max_hp * 0.3:
            actions.append(rule.action)
        elif rule.trigger == "mana < X" and player.mana < player.max_mana * 0.3:
            actions.append(rule.action)
        elif rule.trigger == "target dead" and player.target != null and player.target.hp <= 0:
            actions.append(rule.action)
    return actions
