extends CharacterBody3D

const SPEED = 5.0
const JUMP_VELOCITY = 4.5
const ROTATE_MOUSE_SPEED = 0.03
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

@onready var anim_player = $hero_014/AnimationPlayer
@onready var bullet_gun = load("res://bullet.tscn")
@onready var ray_bullet = $RayCast3D
@onready var ray_big_gun = $RayCast3D2
@onready var bullet_gun_count_lbl = $"../CanvasLayer/bullet_gun_count"
@onready var life_count_lbl = $"../CanvasLayer/Label"

@onready var big_gun = $"hero_014/Арматура/Skeleton3D/big_gun/big_gun"
@onready var game_over_label = $"../CanvasLayer/GameOverLabel"

var GUN = null
var hp = 10
var bullet_gun_count = 100
var life_count = 10

const TIME_GUN_RECHARGE = 0.5
var recharge_gun_timer = TIME_GUN_RECHARGE

const TIME_BIG_GUN_RECHARGE = 1.0
var recharge_big_gun_timer = TIME_BIG_GUN_RECHARGE
func update_ui():
	bullet_gun_count_lbl.text = str(bullet_gun_count)
	life_count_lbl.text = str(life_count)

func _ready():
	big_gun.visible = false
	game_over_label.visible = false  # Приховуємо напис, але не змінюємо тип

	update_ui()

func _physics_process(delta: float) -> void:
	apply_gravity(delta)
	handle_movement()
	handle_collisions()
	update_timers(delta)

func apply_gravity(delta):
	if not is_on_floor():
		velocity.y -= gravity * delta

func handle_movement():
	var input_dir = Input.get_vector("ui_right", "ui_left", "ui_down", "ui_up")
	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	if direction:
		velocity.x = direction.x * SPEED
		velocity.z = direction.z * SPEED
		anim_player.play("go-g0")
	else:
		velocity.x = 0
		velocity.z = 0
	
	move_and_slide()

func handle_collisions():
	for ind in range(get_slide_collision_count()):
		var col = get_slide_collision(ind).get_collider()
		if col and col.name == "big_gun":
			col.queue_free()
			big_gun.visible = true

func update_timers(delta):
	recharge_gun_timer += delta
	recharge_big_gun_timer += delta

func _input(event):
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	elif Input.is_action_just_pressed("ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	elif event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotate_y(-event.relative.x * ROTATE_MOUSE_SPEED)
	
	handle_weapon_switch()
	handle_shooting()

func handle_weapon_switch():
	if Input.is_action_just_pressed("get_gun"):
		if GUN == null:
			anim_player.play("get_gun")
			GUN = "gun"
		elif GUN == "gun":
			anim_player.play("big_gun")
			GUN = "big_gun"
		elif GUN == "big_gun":
			GUN = null

func handle_shooting():
	if Input.is_action_just_pressed("shoot"):
		if GUN == "gun" and recharge_gun_timer >= TIME_GUN_RECHARGE:
			shoot_bullet()
			#anim_player.play("get_gun")
		elif GUN == "big_gun" and recharge_big_gun_timer >= TIME_BIG_GUN_RECHARGE:
			shoot_big_gun()
			#anim_player.play("big_gun")

func shoot_bullet():
	var inst = bullet_gun.instantiate()
	inst.position = ray_bullet.global_position
	inst.transform.basis = ray_bullet.global_transform.basis
	get_tree().get_root().add_child(inst)

	bullet_gun_count -= 1
	update_ui()
	recharge_gun_timer = 0

#func shoot_big_gun():
	#if recharge_big_gun_timer < TIME_BIG_GUN_RECHARGE:
		#return
	#
	#if ray_big_gun.is_colliding():
		#var collide_obj = ray_big_gun.get_collider()
		#if collide_obj and collide_obj.is_in_group("enemy"):
			#collide_obj.damage(3)
	#
	#var inst = bullet_gun.instantiate()
	#inst.position = ray_big_gun.global_position
	#inst.transform.basis = ray_big_gun.global_transform.basis
	#get_tree().get_root().add_child(inst)
#
	#recharge_big_gun_timer = 0
func shoot_big_gun():
	if recharge_big_gun_timer < TIME_BIG_GUN_RECHARGE:
		return
	
	if ray_big_gun.is_colliding():
		var collide_obj = ray_big_gun.get_collider()
		if collide_obj and collide_obj.is_in_group("enemy"):  # Переконуємося, що це ворог
			if collide_obj.has_method("damage"):  # Перевіряємо, чи є у нього метод `damage()`
				collide_obj.damage(3)  # Передаємо аргумент
	
	var inst = bullet_gun.instantiate()
	inst.position = ray_big_gun.global_position
	inst.transform.basis = ray_big_gun.global_transform.basis
	get_tree().get_root().add_child(inst)

	recharge_big_gun_timer = 0

func damage(amount=1):
	hp -= amount
	life_count -= amount
	update_ui()

	if hp <= 0:
		show_game_over()

func check_victory():
	# Отримуємо всіх ворогів у групі "enemy"
	var enemies = get_tree().get_nodes_in_group("enemy")
	if enemies.is_empty():
		show_victory()

func show_game_over():
	game_over_label.text = "Ти програв"
	game_over_label.visible = true
	
	# Затримка перед переходом на початкову сцену
	await get_tree().create_timer(1.0).timeout  
	get_tree().change_scene_to_file("res://menu.tscn")  # Вкажіть правильний шлях до меню


func show_victory():
	game_over_label.text = "Ти виграв"
	game_over_label.visible = true
	
	await get_tree().create_timer(2.0).timeout  
	get_tree().change_scene_to_file("res://menu.tscn")  # Вкажіть правильний шлях до меню
