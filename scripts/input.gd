extends Node

const DEAD_ZONE := 12.0

func smer() -> Vector2:
    var mouse_pos: Vector2 = get_viewport().get_mouse_position()
    var player_pos: Vector2 = get_parent().get_node("Player").global_position
    var direction: Vector2 = mouse_pos - player_pos
    if direction.length() < DEAD_ZONE:
        return Vector2.ZERO
    return direction.normalized()

func chce_krok() -> bool:
    return Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT)

func zpetny_smer() -> Vector2:
    var direction: Vector2 = Vector2.ZERO
    if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
        direction.y -= 1.0
    if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
        direction.y += 1.0
    if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
        direction.x -= 1.0
    if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
        direction.x += 1.0
    return direction.normalized()
