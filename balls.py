from pico2d import *
import random

# Game object class here
class Grass:
    # 생성자 함수 : 객체의 초기 상태를 설정
    def __init__(self):
        #모양없는 납작한 붕어빵의 초기모습 결정
        self.image = load_image('grass.png')  

    def draw(self):
        self.image.draw(400, 30)  

    def update(self):
        pass


class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90  
        self.frame = random.randint(0, 7)  
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8  
        self.x += 5  
        if self.x > 800:  
            self.x = 0 

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)  # 특정 프레임의 이미지를 그린다


class Ball:
    def __init__(self):
    
        if random.randint(0, 1) == 0:
            self.image = load_image('ball21x21.png')  
            self.size = 21
        else:
            self.image = load_image('ball41x41.png')  
            self.size = 41
        
        self.x = random.randint(0, 800)  
        self.y = 599  
        self.speed = random.randint(5, 15)  
    
    def update(self):
        
        if self.y > 30 + self.size // 2:  
            self.y -= self.speed
        else:
            self.y = 30 + self.size // 2  

    def draw(self):
        
        self.image.draw(self.x, self.y)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global running
    global grass
    global team
    global balls

    running = True
    grass = Grass()  
    team = [Boy() for _ in range(10)]  
    balls = [Ball() for _ in range(20)]  


def update_world():
    grass.update()  
    for boy in team:
        boy.update()  
    for ball in balls:
        ball.update()  


def render_world():
    clear_canvas()
    grass.draw()  
    for boy in team:
        boy.draw()  
    for ball in balls:
        ball.draw()  
    update_canvas()


open_canvas()

# initialization code
reset_world()

# game main loop code
while running:
    handle_events()
    update_world()  # 상태 업데이트
    render_world()  # 그 결과를 화면에 렌더링
    delay(0.05)

# finalization code
close_canvas()
