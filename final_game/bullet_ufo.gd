extends RigidBody3D

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
		if body.name=="HERO":
			body.damage()
		queue_free()# видалити кулю
	if timer>=time_disaper:
		queue_free()
	timer+=delta
		
		
		
		
		
	
