extends CharacterBody3D

const rotate_value = 0.05
const SPEED = 5.0
const JUMP_VELOCITY = 4.5
@onready var start_pos = position
@export var pash_length = 8
var is_rotate = false
var rotate_angle = 0
var hp = 3 # 3 рази може попасти куля, після цього зникає

# Стан патрулює і нападає
const STATE_PATROOL = 0
const STATE_ATACK = 1
var STATE = STATE_PATROOL
var aim = null

var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")
@onready var bullet_gun = load("res://bullet_ufo.tscn")
@onready var ray_bullet = $ufo_gun/RayCast3D

# Постріл 
const time_gun_recharge = 0.5
var recharge_gun_timer = time_gun_recharge

func _physics_process(delta: float) -> void:
	# Додаємо гравітацію
	if not is_on_floor():
		velocity += get_gravity() * delta

	# Оновлюємо таймер перезарядки
	if recharge_gun_timer < time_gun_recharge:
		recharge_gun_timer += delta

	var direction = (transform.basis * Vector3.FORWARD).normalized()
	if STATE == STATE_PATROOL:
		if start_pos.distance_to(position) >= pash_length / 2:
			is_rotate = true

		if is_rotate:
			rotate_y(rotate_value)
			rotate_angle += rotate_value
			if rotate_angle >= deg_to_rad(180):
				is_rotate = false
				rotate_angle = 0
			else:
				direction = Vector3.ZERO

	if STATE == STATE_ATACK:
		look_at(aim.global_transform.origin)
		if recharge_gun_timer >= time_gun_recharge:
			shoot()
			recharge_gun_timer = 0  # Скидаємо таймер після пострілу

	if direction:
		velocity.x = direction.x * SPEED
		velocity.z = direction.z * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		velocity.z = move_toward(velocity.z, 0, SPEED)

	move_and_slide()

func shoot():
	var inst = bullet_gun.instantiate()
	inst.position = ray_bullet.global_position
	inst.transform.basis = ray_bullet.global_transform.basis
	get_tree().get_root().add_child(inst)

#func damage(damage=1):
	#hp -= damage
	#if hp <= 0:
		#queue_free()
		
func damage(amount):
	hp -= amount
	if hp <= 0:
		queue_free()
		get_tree().call_group("player", "check_victory")  # Викликаємо перевірку перемоги


func _on_area_3d_body_exited(body: Node3D) -> void:
	if body.name == "HERO":
		aim = body
		STATE = STATE_ATACK
