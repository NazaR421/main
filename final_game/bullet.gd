extends RigidBody3D
@onready var particles = load("res://sparks_shoot.tscn")
var speed=20
const time_disaper=2 #таймер зникнення
var timer =0 # змінна, яка буде рахувати
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	apply_central_impulse(transform.basis * Vector3(0, 0, speed))

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	var bodies = get_colliding_bodies()
	#print(bodies)
	for body in bodies:
		if body.is_in_group("enemy"): # якщо куля влучила в енемі
			body.queue_free() # видатити його
			body.damage(1)
		var sparks= particles.instantiate()
		sparks.position = body.global_position
		get_tree().get_root().add_child(sparks)
		queue_free()# видалити кулю
	if timer>=time_disaper:
		queue_free()
	timer+=delta
		
		
		
		
		
	
