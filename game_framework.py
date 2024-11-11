import time

running = None
stack = None
frame_time = 0.0

def change_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    stack.append(mode)
    mode.init()

def push_mode(mode):
    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(mode)
    mode.init()

def pop_mode():
    global stack
    if len(stack) > 0:
        stack[-1].finish()
        stack.pop()
    if len(stack) > 0:
        stack[-1].resume()

def quit():
    global running
    running = False

def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]
    start_mode.init()

    current_time = time.time()

    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        # frame_time 업데이트
        new_time = time.time()
        frame_time = new_time - current_time
        current_time = new_time
