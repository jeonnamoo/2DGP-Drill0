from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
boy = load_image('character.png')

def draw_boy(x, y):
    clear_canvas_now()
    grass.draw_now(400, 30)
    boy.draw_now(x, y)
    delay(0.1)

def run_rectangle():
    print('RECTANGLE')
    run_bottom()
    run_right()
    run_top()
    run_left()

def run_triangle():
    print('TRIANGLE')
    run_bottom()
    run_right()
    run_cross()

def run_circle():
    print('CIRCLE')

    r, cx, cy = 300, 800 // 2, 600 // 2

    for d in range(0, 360, 10):
        x = r * math.cos(math.radians(d)) + cx
        y = r * math.sin(math.radians(d)) + cy
        draw_boy(x, y)

def run_top():
    print('TOP')
    for x in range(800, 0, -10):
        draw_boy(x, 550)

def run_right():
    print('RIGHT')
    for y in range(0, 600, 10):
        draw_boy(750, y)

def run_bottom():
    print('BOTTOM')
    for x in range(0, 800, 10):
        draw_boy(x, 90)

def run_left():
    print('LEFT')
    for y in range(600, 0, -10):
        draw_boy(50, y)

def run_cross():
    print('CROSS')
    for x, y in zip(range(800, 0, -15), range(600, 0, -10)):
        draw_boy(x, y)

while True:
    run_circle()
    run_rectangle()
    run_triangle()
    break

close_canvas()
