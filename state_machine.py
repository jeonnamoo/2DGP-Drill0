from sdl2 import SDLK_SPACE, SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

def space_down(e):  # e가 space down인지 판단? True or False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):  # e가 time out인지 판단?
    return e[0] == 'TIME_OUT'

def start_event(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class StateMachine:
    def __init__(self, obj):
        self.obj = obj
        self.event_q = []

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.obj, ('START', 0))

    def update(self):
        self.cur_state.do(self.obj)
        if self.event_q:
            e = self.event_q.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    self.cur_state.exit(self.obj, e)
                    self.cur_state = next_state
                    self.cur_state.enter(self.obj, e)
                    return

    def draw(self):
        self.cur_state.draw(self.obj)

    def add_event(self, e):
        self.event_q.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions
