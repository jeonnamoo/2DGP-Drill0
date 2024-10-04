from pico2d import *

import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand_arrow = load_image('hand_arrow.png')

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass

def move_character_with_mouse():
    global x, y, target_x, target_y, direction

    if x < target_x:
        x += speed
        direction = 1
    elif x > target_x:
        x -= speed
        direction = -1

    if y < target_y:
        y += speed
    elif y > target_y:
        y -=speed

    if abs(x - target_x) < speed and abs(y - target_y) < speed:
        target_x, target_y = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)

hide_cursor()



running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
target_x, target_y = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)
frame = 0
direction= 1
speed = 1

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    hand_arrow.draw(target_x,target_y)

    if direction == 1:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    else:
        character.clip_composite_draw(frame * 100, 100 *1, 100, 100, 0, 'h', x, y, 100, 100)

    update_canvas()
    move_character_with_mouse()
    frame = (frame + 1) % 8

    handle_events()

close_canvas()




