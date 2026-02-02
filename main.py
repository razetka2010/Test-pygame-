import turtle
import time
import random
import pygame

pygame.init()

# Настройки экрана
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

# Голова змейки
head = turtle.Turtle()
head.shape("square")
head.color("white")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Еда
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

segments = []

# Функции движения
def go_up():
    if head.direction != "down": head.direction = "up"
def go_down():
    if head.direction != "up": head.direction = "down"
def go_left():
    if head.direction != "right": head.direction = "left"
def go_right():
    if head.direction != "left": head.direction = "right"

def move():
    if head.direction == "up": head.sety(head.ycor() + 20)
    if head.direction == "down": head.sety(head.ycor() - 20)
    if head.direction == "left": head.setx(head.xcor() - 20)
    if head.direction == "right": head.setx(head.xcor() + 20)

# Управление
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

# Основной цикл
while True:
    screen.update()
    
    # Проверка столкновения с едой
    if head.distance(food) < 20:
        food.goto(random.randint(-280, 280), random.randint(-280, 280))
        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

    # Движение хвоста
    for i in range(len(segments)-1, 0, -1):
        segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()
    
    # Смерть при выходе за границы
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"
        for s in segments: s.goto(1000, 1000)
        segments.clear()

    time.sleep(0.1)
