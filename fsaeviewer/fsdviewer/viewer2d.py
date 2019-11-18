import pygame
import math
from threading import Thread

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 10)
ORANGE = (255, 69, 0)


class Cone:
    def __init__(self, color, x, y, size = 5):
        self.x = x
        self.y = y
        self.color = color
        self.size = size



class Line:
    def __init__(self, cone1, cone2, color, size):
        self.cone1 = cone1
        self.cone2 = cone2
        self.color = color
        self.size = size



class LineMiddle:
    def __init__(self, cone1, cone2, cone3, cone4, color, size):
        self.cone1 = cone1
        self.cone2 = cone2
        self.cone3 = cone3
        self.cone4 = cone4
        self.color = color
        self.size = size


class Car:
    def __init__(self, x, y, rot, color="black"):
        self.x = x
        self.y = y
        self.rot = rot
        self.color = color

simple_map = [Cone("blue", 50, 50), Cone("blue", 150, 50), Cone("yellow", 50, 120), Cone("yellow", 150, 120)]
simple_lines = [Line(0, 1, "red", 1), Line(0, 2, "green", 2)]
simple_middleLines = [LineMiddle(0, 2, 0, 1, "blue", 3)]
simple_cars = [Car(50, 85, 0)]

cones = []
lines = []
middleLines = []
cars = []


pygame.init()
# Set the width and height of the screen [width, height]
size = (700, 700)
screen = pygame.display.set_mode(size)
cam_pos = [0,0]
pygame.display.set_caption("E-Racing Driverless 2d Sim")
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
zoom = 1

def draw(cones, lines, middleLines, cars):

    global zoom
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                if zoom < 10:
                    zoom += 1
            if event.key == pygame.K_k:
                if zoom > 1:
                    zoom -= 1
            if event.key == pygame.K_a:
                cam_pos[0] += 8
            if event.key == pygame.K_d:
                cam_pos[0] -= 8
            if event.key == pygame.K_w:
                cam_pos[1] += 8
            if event.key == pygame.K_s:
                cam_pos[1] -= 8

    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)

    # --- Drawing code should go here

    # lines drawing
    for line in lines:
        pos1 = [(cones[line.cone1].x + cam_pos[0])*zoom, (cones[line.cone1].y + cam_pos[1])*zoom]
        pos2 = [(cones[line.cone2].x + cam_pos[0])*zoom, (cones[line.cone2].y + cam_pos[1])*zoom]
        if line.color == "red":
            pygame.draw.line(screen, RED, pos1, pos2, line.size*zoom)
        if line.color == "green":
            pygame.draw.line(screen, GREEN, pos1, pos2, line.size*zoom)
        if line.color == "yellow":
            pygame.draw.line(screen, YELLOW, pos1, pos2, line.size*zoom)
        if line.color == "blue":
            pygame.draw.line(screen, BLUE, pos1, pos2, line.size*zoom)
        if line.color == "orange":
            pygame.draw.line(screen, ORANGE, pos1, pos2, line.size*zoom)

    for line in middleLines:
        pos1 = [(cones[line.cone1].x + cam_pos[0])*zoom, (cones[line.cone1].y + cam_pos[1])*zoom]
        pos2 = [(cones[line.cone2].x + cam_pos[0])*zoom, (cones[line.cone2].y + cam_pos[1])*zoom]
        pos3 = [(cones[line.cone3].x + cam_pos[0])*zoom, (cones[line.cone3].y + cam_pos[1])*zoom]
        pos4 = [(cones[line.cone4].x + cam_pos[0])*zoom, (cones[line.cone4].y + cam_pos[1])*zoom]
        pos1[0] = (pos1[0] + pos2[0])/2
        pos1[1] = (pos1[1] + pos2[1])/2
        pos2[0] = (pos3[0] + pos4[0])/2
        pos2[1] = (pos4[1] + pos4[1])/2
        if line.color == "red":
            pygame.draw.line(screen, RED, pos1, pos2, line.size*zoom)
        if line.color == "green":
            pygame.draw.line(screen, GREEN, pos1, pos2, line.size*zoom)
        if line.color == "yellow":
            pygame.draw.line(screen, YELLOW, pos1, pos2, line.size*zoom)
        if line.color == "blue":
            pygame.draw.line(screen, BLUE, pos1, pos2, line.size*zoom)
        if line.color == "orange":
            pygame.draw.line(screen, ORANGE, pos1, pos2, line.size*zoom)

    # cones drawing

    for cone in cones:
        if cone.color == "blue":
            pygame.draw.circle(screen, BLUE, [(cone.x + cam_pos[0])*zoom, (cone.y + cam_pos[1])*zoom], cone.size*zoom)
        elif cone.color == "yellow":
            pygame.draw.circle(screen, YELLOW, [(cone.x + cam_pos[0])*zoom, (cone.y + cam_pos[1])*zoom], cone.size*zoom)
        elif cone.color == "orange":
            pygame.draw.circle(screen, ORANGE, [(cone.x + cam_pos[0])*zoom, (cone.y + cam_pos[1])*zoom], cone.size*zoom)
        elif cone.color == "red":
            pygame.draw.circle(screen, RED, [(cone.x + cam_pos[0])*zoom, (cone.y + cam_pos[1])*zoom], cone.size*zoom)
        elif cone.color == "green":
            pygame.draw.circle(screen, GREEN, [(cone.x + cam_pos[0])*zoom, (cone.y + cam_pos[1])*zoom], cone.size*zoom)
        elif cone.color == "black":
            pygame.draw.circle(screen, BLACK, [(cone.x + cam_pos[0])*zoom, (cone.y + cam_pos[1])*zoom], cone.size*zoom)


    # car drawing


    for car in cars:
        p1o = [-15, 20]
        p1 = [-15, 20]
        p1[0] = p1o[0]*math.cos(car.rot) - p1o[1]*math.sin(car.rot)
        p1[1] = p1o[0]*math.sin(car.rot) + p1o[1]*math.cos(car.rot)
        p1[0] += car.x
        p1[1] += car.y
        p1[0] = (p1[0] + cam_pos[0])*zoom
        p1[1] = (p1[1] + cam_pos[1])*zoom
        p2 = [15, 20]
        p2o = [15, 20]
        p2[0] = p2o[0]*math.cos(car.rot) - p2o[1]*math.sin(car.rot)
        p2[1] = p2o[0]*math.sin(car.rot) + p2o[1]*math.cos(car.rot)
        p2[0] += car.x
        p2[1] += car.y
        p2[0] = (p2[0] + cam_pos[0])*zoom
        p2[1] = (p2[1] + cam_pos[1])*zoom
        p3 = [0, -20]
        p3o = [0, -20]
        p3[0] = p3o[0]*math.cos(car.rot) - p3o[1]*math.sin(car.rot)
        p3[1] = p3o[0]*math.sin(car.rot) + p3o[1]*math.cos(car.rot)
        p3[0] += car.x
        p3[1] += car.y
        p3[0] = (p3[0] + cam_pos[0])*zoom
        p3[1] = (p3[1] + cam_pos[1])*zoom
        if car.color == "black":
            pygame.draw.polygon(screen, BLACK, [p1, p2, p3])
        if car.color == "blue":
            pygame.draw.polygon(screen, BLUE, [p1, p2, p3])
        if car.color == "green":
            pygame.draw.polygon(screen, GREEN, [p1, p2, p3])




    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
def quit():
    pygame.quit()


