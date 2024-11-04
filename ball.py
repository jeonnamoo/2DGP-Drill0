import game_world


def update(self):
    self.x += self.velocity

    if self.x < 25 or self.x > 800 - 25:
        game_world.remove_object(self)