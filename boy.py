from pico2d import load_image, get_time
from state_machine import StateMachine, space_down, time_out, left_up, right_down, right_up, left_down, start_event

class Idle:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0  # Idle 상태 초기화
        boy.start_time = get_time()  # 현재 시간 저장
        boy.size_multiplier = 1  # 기본 크기로 설정

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8  # 프레임 증가
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        size = int(100 * boy.size_multiplier)  # 크기 조정
        boy.image.clip_draw(boy.frame * 100, 300, 100, 100, boy.x, boy.y)  # Idle 애니메이션


class AutoRun:
    @staticmethod
    def enter(boy, e):
        boy.speed = 10  # 자동 런 속도
        boy.size_multiplier = 1.5  # 크기 확대
        boy.start_time = get_time()  # 자동 런 시작 시간
        boy.dir = 1  # 초기 방향 오른쪽
        boy.frame = 0  # 초기 프레임

    @staticmethod
    def exit(boy, e):
        boy.speed = 5  # 기본 속도로 복귀
        boy.size_multiplier = 1  # 원래 크기로 복귀

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * boy.speed

        # 화면 끝에 닿으면 방향 전환
        if boy.x > 800:  # 화면 오른쪽 끝
            boy.dir = -1
        elif boy.x < 0:  # 화면 왼쪽 끝
            boy.dir = 1

        # 5초가 지나면 Idle 상태로 전환
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        size = int(150 * boy.size_multiplier)  # 크기 조정
        if boy.dir == 1:  # 오른쪽으로 이동할 때
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)  # 오른쪽 달리기 애니메이션
        else:  # 왼쪽으로 이동할 때
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)  # 왼쪽 달리기 애니메이션


class Run:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0  # 초기화
        if right_down(e):
            boy.dir = 1  # 오른쪽
        elif left_down(e):
            boy.dir = -1  # 왼쪽
        boy.size_multiplier = 1  # Run 상태에서는 크기 유지

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
        size = int(100 * boy.size_multiplier)  # 크기 조정
        if boy.dir == 1:  # 오른쪽으로 이동할 때
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)  # 오른쪽 달리기 애니메이션
        else:  # 왼쪽으로 이동할 때
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)  # 왼쪽 달리기 애니메이션


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.image = load_image('animation_sheet.png')
        self.size_multiplier = 1  # 기본 크기 배수
        self.state_machine = StateMachine(self)  # 소년 객체의 state machine 생성
        self.state_machine.start(Idle)  # 초기 상태가 Idle
        self.state_machine.set_transitions(
            {
                AutoRun: {time_out: Idle, right_down: Run, left_down: Run},  # AutoRun에서 Idle, Run으로 전환
                Idle: {start_event: AutoRun},  # Idle에서 AutoRun으로 전환
                Run: {right_down: Run, left_down: Run, start_event: AutoRun}  # Run 상태에서 AutoRun으로 전환
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
