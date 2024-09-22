import turtle

def move_up():
    turtle.setheading(90)
    turtle.forward(50)

def move_down():
    turtle.setheading(270)
    turtle.forward(50)

def move_left():
    turtle.setheading(180)
    turtle.forward(50)

def move_right():
    turtle.setheading(0)
    turtle.forward(50)


def restart():
    turtle.reset()

turtle.shape('turtle')

turtle.onkey(move_up, 'w')  
turtle.onkey(move_down, 's')
turtle.onkey(move_left, 'a')  
turtle.onkey(move_right, 'd')
turtle.listen()

turtle.onkey(restart, 'Escape')
turtle.listen()
