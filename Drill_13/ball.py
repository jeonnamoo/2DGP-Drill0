import server
from pico2d import *
import game_world
import random

class Ball:
    image = None

    def __init__(self, x=None, y=None):
        if Ball.image is None:
            Ball.image = load_image('ball21x21.png')
        self.x = x if x else random.randint(0, server.background.w)
        self.y = y if y else random.randint(0, server.background.h)

    def draw(self):
        screen_x = self.x - server.background.window_left
        screen_y = self.y - server.background.window_bottom
        self.image.draw(screen_x, screen_y)
        draw_rectangle(*self.get_bb(screen_x, screen_y))

    def update(self):
        pass  # 공은 고정되어 있으므로 update는 빈 함수

    def get_bb(self, screen_x=None, screen_y=None):
        if screen_x is None or screen_y is None:
            return self.x - 10, self.y - 10, self.x + 10, self.y + 10
        return screen_x - 10, screen_y - 10, screen_x + 10, screen_y + 10

    def handle_collision(self, group, other):
        if other is server.boy:
            game_world.remove_object(self)
