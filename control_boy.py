from pico2d import *
import game_world
from grass import Grass
from boy import Boy

def handle_events():
    global running, boy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)

def reset_world():
    global boy, running
    running = True

    BACKGROUND_LAYER = 0
    BOY_LAYER = 1
    FOREGROUND_LAYER = 2

    game_world.world = [[], [], []]

    # 뒤쪽 잔디 (y=70)
    grass_background = Grass(y=50)
    game_world.add_object(grass_background, BACKGROUND_LAYER)

    boy = Boy()
    game_world.add_object(boy, BOY_LAYER)

    # 앞쪽 잔디 (y=50)
    grass_foreground = Grass(y=30)
    game_world.add_object(grass_foreground, FOREGROUND_LAYER)

def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

open_canvas()
reset_world()

running = True
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
