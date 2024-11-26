# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *
import game_framework

# Bird Fly Speed
PIXEL_PER_METER = (10.0 / 0.5)  # 10 pixel 50 cm
FLY_SPEED_KMPH = 25.0  # Km / Hour
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.8 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

# 프레임 정보
FRAME_WIDTH = 182
FRAME_HEIGHT = 168
FRAMES_PER_ROW = 5
TOTAL_FRAMES = 15

class Bird:
    def __init__(self):
        self.x, self.y = 400, 300
        self.image = load_image('bird_animation.png')
        self.frame = 0
        self.dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.speed = FLY_SPEED_PPS

    def update(self):
        # 애니메이션 프레임 업데이트
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % TOTAL_FRAMES

        # 위치 업데이트
        self.x += self.dir * self.speed * game_framework.frame_time

        # 화면 경계를 넘으면 방향 반전
        if self.x > 1600:
            self.dir = -1
        elif self.x < 0:
            self.dir = 1

    def draw(self):
        # 현재 프레임에 대한 좌표 계산
        current_frame = int(self.frame)
        row = current_frame // FRAMES_PER_ROW
        col = current_frame % FRAMES_PER_ROW
        frame_x = col * FRAME_WIDTH
        frame_y = (2 - row) * FRAME_HEIGHT  # 이미지의 아래쪽부터 계산

        if self.dir == 1:
            # 오른쪽을 향할 때
            self.image.clip_draw(frame_x, frame_y, FRAME_WIDTH, FRAME_HEIGHT, self.x, self.y)
        else:
            # 왼쪽을 향할 때, 이미지 플립
            self.image.clip_composite_draw(frame_x, frame_y, FRAME_WIDTH, FRAME_HEIGHT, 0, 'h', self.x, self.y, FRAME_WIDTH, FRAME_HEIGHT)

    def handle_event(self, event):
        pass  # 이벤트 처리가 필요하지 않음
