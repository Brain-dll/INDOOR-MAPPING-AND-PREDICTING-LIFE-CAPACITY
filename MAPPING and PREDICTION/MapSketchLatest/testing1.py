import turtle
import random
import time
import os



screen = turtle.Screen()
screen.bgcolor('gray')
rootwindow = screen.getcanvas().winfo_toplevel()
rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
rootwindow.call('wm', 'attributes', '.', '-topmost', '0')

radius = 5

myPen = turtle.Turtle()
myPen.color('red')
myPen.width(5)
myPen.speed(0)
myPen.hideturtle()


myPen.penup()
myPen.setpos(0,-radius)
myPen.pendown()
myPen.begin_fill()
myPen.circle(radius)
myPen.end_fill()
myPen.penup()
    

myPen.speed(1)
myPen.pendown()

botX = 100
botY = 100
myPen.setpos(botX, botY)

botY += 100
myPen.setpos(botX, botY)  

turtle.mainloop()






