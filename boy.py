from pico2d import *
import game_world

class Boy:
    def __init__(self):
        self.x, self.y = 400, 60
        self.image = load_image('animation_sheet.png')
        self.frame = 0
        self.dir = 0
        self.velocity = 0

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.velocity
        if self.x < 25:
            self.x = 25
        elif self.x > 775:
            self.x = 775

    def draw(self):
        if self.velocity == 0:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        elif self.velocity > 0:
            self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.velocity += 5
            elif event.key == SDLK_LEFT:
                self.velocity -= 5
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.velocity -= 5
            elif event.key == SDLK_LEFT:
                self.velocity += 5
