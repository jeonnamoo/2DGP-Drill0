import random
import json
import os

from pico2d import *
import game_framework
import game_world

import server
from ball import Ball
from boy import Boy

# fill here
from background import FixedBackground as Background




def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.boy.handle_event(event)



def init():
    server.background = Background()
    game_world.add_object(server.background, 0)

    server.boy = Boy()
    game_world.add_object(server.boy, 1)

    # 공 100개 생성 및 추가
    for _ in range(100):
        ball = Ball()
        game_world.add_object(ball, 1)
        game_world.add_collision_pair('boy:ball', server.boy, ball)  # 충돌 그룹 이름 추가


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass



