# game_world.py
# Managing objects in multiple layers

world = [[], [], []]  # 3 layers: background, middle, foreground

def add_object(o, depth):
    world[depth].append(o)

def update():
    for layer in world:
        for obj in layer:
            obj.update()

def render():
    for layer in world:
        for obj in layer:
            obj.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    print("Error: Tried to remove a non-existent object")
