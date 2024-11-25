from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode


# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk', 'Idle']


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/" + name + " (%d)" % i + ".png") for i in range(1, 11)]
            Zombie.font = load_font('ENCR10B.TTF', 40)
            Zombie.marker_image = load_image('hand_arrow.png')

    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(100, 1180)
        self.y = y if y else random.randint(100, 924)
        self.load_images()
        self.dir = 0.0  # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 'Idle'
        self.ball_count = 0
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()
        self.patrol_locations = [(43, 274), (1118, 274), (1050, 494), (575, 804), (235, 991), (575, 804), (1050, 494),
                                 (1118, 274)]
        self.loc_no = 0

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()  # BehaviorTree 실행

    def draw(self):
        Zombie.marker_image.draw(self.tx - 10, self.ty - 10)
        if math.cos(self.dir) < 0:
            Zombie.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            Zombie.images[self.state][int(self.frame)].draw(self.x, self.y, 100, 100)
        self.font.draw(self.x - 10, self.y + 60, f'{self.ball_count}', (0, 0, 255))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'zombie:ball':
            self.ball_count += 1

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def move_slightly_from(self, tx, ty):
        self.dir = math.atan2(self.y - ty, self.x - tx)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx, self.ty = random.randint(100, 1280 - 100), random.randint(100, 1024 - 100)
        return BehaviorTree.SUCCESS

    def is_boy_nearby(self, r):
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_boy(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.boy.x, play_mode.boy.y)

        # 공 개수가 많은 경우에만 추적
        if self.ball_count > play_mode.boy.ball_count:
            if self.distance_less_than(self.x, self.y, play_mode.boy.x, play_mode.boy.y, r):
                return BehaviorTree.SUCCESS
            return BehaviorTree.RUNNING
        return BehaviorTree.FAIL  # 공 개수가 많지 않은 경우 추적하지 않음

    def escape_from_boy(self, r=7):
        self.state = 'Walk'
        print(f"도망 중: 현재 위치 ({self.x:.2f}, {self.y:.2f}), 소년 위치 ({play_mode.boy.x:.2f}, {play_mode.boy.y:.2f})")

        # 소년으로부터 반대 방향으로 이동
        self.move_slightly_from(play_mode.boy.x, play_mode.boy.y)

        # 공 개수가 적은 경우 도망
        if self.ball_count < play_mode.boy.ball_count:
            # 충분히 멀어진 경우 Wander 상태로 전환
            if not self.distance_less_than(self.x, self.y, play_mode.boy.x, play_mode.boy.y, r):
                print("도망 성공, Wander 상태로 전환")
                return BehaviorTree.SUCCESS
            return BehaviorTree.RUNNING  # 아직 멀어지지 않음
        return BehaviorTree.FAIL  # 공 개수가 적지 않은 경우 도망하지 않음

    def get_patrol_location(self):
        self.tx, self.ty = self.patrol_locations[self.loc_no]
        self.loc_no = (self.loc_no + 1) % len(self.patrol_locations)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # 배회 행동
        wander_action = Action('Set random location', self.set_random_location)
        move_action = Action('Move to', self.move_to)
        wander_sequence = Sequence('배회', wander_action, move_action)

        # 도망 행동
        escape_action = Action('도망', self.escape_from_boy)
        escape_sequence = Sequence('도망', escape_action)

        # 추적 행동
        chase_action = Action('소년 추적', self.move_to_boy)
        chase_sequence = Sequence('추적', chase_action)

        # 소년이 근처에 있는 경우 (추적 또는 도망)
        is_near_boy = Condition('소년이 근처에 있는가?', self.is_boy_nearby, 7)
        near_boy_selector = Selector('근처에서 행동 선택', escape_sequence, chase_sequence)

        # 최상위 Selector 노드 (우선순위: 근처 판단 -> 배회)
        root = Selector('행동 선택', Sequence('근처 확인', is_near_boy, near_boy_selector), wander_sequence)

        self.bt = BehaviorTree(root)


