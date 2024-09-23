from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

x = 400
y = 90
while (x < 800):
    clear_canvas_now()
    grass.draw_now(400, 30)
    character.draw_now(x, y)
    x = x + 2
    delay(0.01)


while(y < 600):
    clear_canvas_now()
    grass.draw_now(400,30)
    character.draw_now(800,y)
    y = y + 2
    delay(0.01)

while(y >90):
    clear_canvas_now()
    grass.draw_now(400,30)
    character.draw_now(x,y)
    x = x - 3
    y = y - 2
    delay(0.01)

while(x<400):
    clear_canvas_now()
    grass.draw_now(400, 30)
    character.draw_now(x, 90)
    x = x + 2
    delay(0.01)


while(x<800):
    clear_canvas_now()
    grass.draw_now(400,30)
    character.draw_now(x,y)
    center_x, center_y = 400,300
    radius = 300
    delay(0.01)



 










    
    

close_canvas()
