import turtle as t
import math as m
import random as r
import time as tm
tscreen = t.Screen()
t.colormode(255)
tscreen.bgcolor((0, 0, 0))
t.color((255, 255, 255))
t.tracer(0)
t.hideturtle()
counter = 0
total_sum = 0
#generate several boids
class Boid:
    def __init__(self, xpos, ypos, vectorx, vectory):
        self.xpos = xpos
        self.ypos = ypos
        magnitude = vectorx * vectorx + vectory * vectory
        self.vectorx = vectorx #/ magnitude * 7
        self.vectory = vectory #/ magnitude * 7
        self.color = (m.floor(magnitude / 100), m.floor(1.275 * magnitude), m.floor(255 * magnitude / 200))
    def update_position(self):
        self.xpos += self.vectorx
        self.ypos += self.vectory
        if (self.xpos < -750):
            self.xpos += 1495
        if (self.xpos > 750):
            self.xpos -= 1495
        if (self.ypos < -375):
            self.ypos += 745
        if (self.ypos > 375):
            self.ypos -= 745
    def update_vector(self):
        global list_boids
        included_count = 0
        included_vectorx = 0
        included_vectory = 0
        average_x = 0
        average_y = 0
        avoid_vectorx = 0
        avoid_vectory = 0
        avoid_count = 0
        for i in list_boids:
            if (str(i) == str(self)):
                continue
            distance = pow(i.xpos - self.xpos, 2) + pow(i.ypos - self.ypos, 2)
            if (distance < 10000): #sight radius
                #get average vector direction and add it to current vector
                included_vectorx += i.vectorx
                included_vectory += i.vectory
                average_x += i.xpos
                average_y += i.ypos
                included_count += 1
                if (distance < 2500):
                    #avoid/move away from boids that are too close
                    xpos_away = -1 * (i.xpos - self.xpos)
                    ypos_away = -1 * (i.ypos - self.ypos)
                    distance_away = 50 - m.sqrt(pow(xpos_away, 2) + pow(ypos_away, 2))
                    vector_multiplier = m.sqrt(pow(distance_away, 2) / (pow(xpos_away, 2) + pow(ypos_away, 2)))
                    avoid_vectorx += xpos_away * vector_multiplier
                    avoid_vectory += ypos_away * vector_multiplier
                    avoid_count += 1
        if (avoid_count > 0):
            avoid_vectorx /= avoid_count
            avoid_vectory /= avoid_count 
        if (included_count > 0):
            average_vectorx = (average_x / included_count - self.xpos) * 0.1
            average_vectory = (average_y / included_count - self.ypos) * 0.1
            included_vectorx /= included_count
            included_vectory /= included_count
            vector_magnitude = m.sqrt(self.vectorx * self.vectorx + self.vectory * self.vectory)
            self.vectorx = (self.vectorx + included_vectorx + avoid_vectorx + average_vectorx) #+ average_vectorx + avoid_vectorx) 
            self.vectory = (self.vectory + included_vectory + avoid_vectory + average_vectory) #+ average_vectory + avoid_vectory)
            distance_ratio = vector_magnitude / m.sqrt(self.vectorx * self.vectorx + self.vectory * self.vectory)
            #self.vectorx *= distance_ratio
            #self.vectory *= distance_ratio
        #get average vector direction and add it to current vector
    def __repr__(self):
        return f"{self.xpos}{self.ypos}{self.vectorx}{self.vectory}"
# x = -750, 750
# y = -375, 375
list_boids = []
list_turtles = []
for i in range(0, 50):
    #calculate unit vector
    vectorx = r.randint(-10, 10)
    vectory = r.randint(-10, 10)
    list_boids.append(Boid(r.randint(-750, 750), r.randint(-375, 375), vectorx, vectory))
    turtle = t.Turtle()
    turtle.hideturtle()
    turtle.up()
    list_turtles.append(turtle) 
def draw_boids():
    global total_sum
    global counter
    time_start = tm.time()
    for i in range(0, len(list_boids)):
        turtle = list_turtles[i]
        turtle.clear()
        boid = list_boids[i]
        boid.update_position()
        turtle.goto(boid.xpos, boid.ypos)
        turtle.dot(15, boid.color)
        boid.update_vector()
    t.update()
    total_sum += (tm.time() - time_start)
    counter += 1
    print(total_sum / counter)
    t.ontimer(draw_boids, 1)
draw_boids()
tscreen.mainloop()