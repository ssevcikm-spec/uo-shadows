extends Node

# Offline activity resolution.
# Returns a dictionary with keys:
#   zisk: int – amount of resources earned (capped per day)
#   xp:   int – experience points awarded.
# The calculation uses the character's relevant skill multiplied by the
# offline duration and an efficiency factor (0.3) to simulate reduced output
# compared to active gameplay. The daily cap limits total offline earnings
# to DAILY_CAP units.

const DAILY_CAP: int = 100
const EFFICIENCY: float = 0.3

func resolve(char, job: String, hours: float) -> Dictionary:
    """Resolve one offline action for the given character.

    `job` can be:
        - "tezba"   – mining skill
        - "vyroba"  – crafting (kovarstvi) skill
        - "boj"     – melee combat skill

    The function never causes death; it returns a safe result.
    """
    var skill_name: String = ""
    match job:
        "tezba":
            skill_name = "tezba"
        "vyroba":
            skill_name = "kovarstvi"
        "boj":
            skill_name = "boj_na_blizko"
        _:
            push_error("offline.gd: unknown job '%s'" % job)
            return {"zisk": 0, "xp": 0}

    var skills = _komponenta("Skills")
    if skills == null:
        push_error("offline.gd: Skills component missing")
        return {"zisk": 0, "xp": 0}

    var skill_val: int = skills.hodnota(skill_name)
    # Base gain = skill value * hours * efficiency factor
    var raw_gain: float = skill_val * hours * EFFICIENCY
    var zisk: int = int(min(raw_gain, DAILY_CAP))

    # Simple XP award proportional to time spent offline
    var xp: int = int(hours)

    return {"zisk": zisk, "xp": xp}

func _komponenta(id: String):
    """Retrieve a component from the parent skeleton (registry)."""
    var parent_node := get_parent()
    if parent_node != null and parent_node.has_method("component"):
        return parent_node.component(id)
    return null
