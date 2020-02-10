import pygame
import math
from threading import Thread

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
magenta = (255,0,255)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 10)
orange = (255, 69, 0)
lime = (0,255,0)
cyan = (0,255,255)
silver = (192,192,192)
gray = (128,128,128) 
maroon = (128,0,0)
green = (0,128,0)

class Point:
    def __init__(self, color, x, y, size = 5):
        self.x = x
        self.y = -y
        self.color = color
        self.size = size


class Line:
    def __init__(self, Point1, Point2, color, size=3):
        self.Point1 = Point1
        self.Point2 = Point2
        self.color = color
        self.size = size


class LineMiddle:
    def __init__(self, Point1, Point2, Point3, Point4, color, size=3):
        self.Point1 = Point1
        self.Point2 = Point2
        self.Point3 = Point3
        self.Point4 = Point4
        self.color = color
        self.size = size

class Car:
    def __init__(self, x, y, rot, steer, color="black", steer_color="magenta"):
        self.x = x
        self.y = -y
        self.rot = -rot+math.pi/2
        self.steer = -steer
        self.color = color
        self.steer_color = steer_color



ZOOM_MAX = 10
ZOOM_MIN = 1
ZOOM_STEP_MOUSE = 0.07
ZOOM_STEP = 0.1
MOVE_STEEP = 5
zoom = 1
screen = None
screen_size = (700, 700)
cam_pos = [350,350]
background_color = None

def init(title="Driverless 2d viewer", background="white", size=(600,600)):
    global screen, screen_size, clock, background_color
    background_color = background
    screen_size = size
    pygame.init()
    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(title)
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

def draw(Points, lines, middleLines, cars):

    global zoom, cam_pos, screen_size, ZOOM_MAX, ZOOM_MIN, ZOOM_STEP, ZOOM_STEP_MOUSE, MOVE_STEEP
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                cam_pos[0] = (screen_size[0]/(2*zoom)) - (pos[0]-cam_pos[0])/zoom
                cam_pos[1] = (screen_size[1]/(2*zoom)) - (pos[1]-cam_pos[1])/zoom
            if event.button == 3:
                cam_pos[0] = screen_size[0]/2
                cam_pos[1] = screen_size[1]/2
                zoom = 1

            if event.button == 4: # mouse wheel up
                pos = pygame.mouse.get_pos()
                zoom += ZOOM_STEP
                cam_pos[0] = (screen_size[0]/(2*zoom)) - (pos[0]-cam_pos[0])/zoom
                cam_pos[1] = (screen_size[1]/(2*zoom)) - (pos[1]-cam_pos[1])/zoom
            if event.button == 5: # mouse wheel down
                pos = pygame.mouse.get_pos()
                zoom -= ZOOM_STEP
                cam_pos[0] = (screen_size[0]/(2*zoom)) - (pos[0]-cam_pos[0])/zoom
                cam_pos[1] = (screen_size[1]/(2*zoom)) - (pos[1]-cam_pos[1])/zoom
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                MOVE_STEEP = MOVE_STEEP * 2
            if event.key == pygame.K_LCTRL:
                ZOOM_STEP = ZOOM_STEP / 2
                ZOOM_STEP_MOUSE  = ZOOM_STEP_MOUSE / 2
            if event.key == pygame.K_g:
                zoom -= ZOOM_STEP
            if event.key == pygame.K_t:
                zoom += ZOOM_STEP
            if event.key == pygame.K_a or event.key == pygame.K_h:
                cam_pos[0] += MOVE_STEEP
            if event.key == pygame.K_d or event.key == pygame.K_l:
                cam_pos[0] -= MOVE_STEEP
            if event.key == pygame.K_w or event.key == pygame.K_k:
                cam_pos[1] += MOVE_STEEP
            if event.key == pygame.K_s or event.key == pygame.K_j:
                cam_pos[1] -= MOVE_STEEP
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                MOVE_STEEP = MOVE_STEEP / 2
            if event.key == pygame.K_LCTRL:
                ZOOM_STEP = ZOOM_STEP * 2
                ZOOM_STEP_MOUSE  = ZOOM_STEP_MOUSE * 2

    zoom = min(zoom, ZOOM_MAX)
    zoom = max(zoom, ZOOM_MIN)

    # clear screen with background color
    screen.fill(eval(background_color))

    # --- Drawing code should go here

    # lines drawing
    for line in lines:
        pos1 = [int((Points[line.Point1].x + cam_pos[0])*zoom), int((Points[line.Point1].y + cam_pos[1])*zoom)]
        pos2 = [int((Points[line.Point2].x + cam_pos[0])*zoom), int((Points[line.Point2].y + cam_pos[1])*zoom)]
        pygame.draw.line(screen, eval(line.color), pos1, pos2, int(line.size*zoom))

    for line in middleLines:
        pos1 = [(Points[line.Point1].x + cam_pos[0])*zoom, (Points[line.Point1].y + cam_pos[1])*zoom]
        pos2 = [(Points[line.Point2].x + cam_pos[0])*zoom, (Points[line.Point2].y + cam_pos[1])*zoom]
        pos3 = [(Points[line.Point3].x + cam_pos[0])*zoom, (Points[line.Point3].y + cam_pos[1])*zoom]
        pos4 = [(Points[line.Point4].x + cam_pos[0])*zoom, (Points[line.Point4].y + cam_pos[1])*zoom]
        pos1[0] = int((pos1[0] + pos2[0])/2)
        pos1[1] = int((pos1[1] + pos2[1])/2)
        pos2[0] = int((pos3[0] + pos4[0])/2)
        pos2[1] = int((pos4[1] + pos4[1])/2)
        pygame.draw.line(screen, eval(line.color), pos1, pos2, int(line.size*zoom))

    # Points drawing

    for point in Points:
        pygame.draw.circle(screen, eval(point.color), [int((point.x + cam_pos[0])*zoom), int((point.y + cam_pos[1])*zoom)],int(point.size*zoom))


    # car drawing
    for car in cars:
        p1o = [-15, 20]
        p1 = [-15, 20]
        p1s = [-5, 0]
        p1f = [-5, 0]
        p1[0] = p1o[0]*math.cos(car.rot) - p1o[1]*math.sin(car.rot)
        p1[1] = p1o[0]*math.sin(car.rot) + p1o[1]*math.cos(car.rot)
        p1[0] += car.x
        p1[1] += car.y
        p1[0] = int((p1[0] + cam_pos[0])*zoom)
        p1[1] = int((p1[1] + cam_pos[1])*zoom)
        p1s[0] = p1f[0]*math.cos(car.steer+car.rot) - p1f[1]*math.sin(car.steer+car.rot)
        p1s[1] = p1f[0]*math.sin(car.steer+car.rot) + p1f[1]*math.cos(car.steer+car.rot)
        p1s[0] += car.x
        p1s[1] += car.y
        p1s[0] = int((p1s[0] + cam_pos[0])*zoom)
        p1s[1] = int((p1s[1] + cam_pos[1])*zoom)
        p2 = [15, 20]
        p2o = [15, 20]
        p2s = [5, 0]
        p2f = [5, 0]
        p2[0] = p2o[0]*math.cos(car.rot) - p2o[1]*math.sin(car.rot)
        p2[1] = p2o[0]*math.sin(car.rot) + p2o[1]*math.cos(car.rot)
        p2[0] += car.x
        p2[1] += car.y
        p2[0] = int((p2[0] + cam_pos[0])*zoom)
        p2[1] = int((p2[1] + cam_pos[1])*zoom)
        p2s[0] = p2f[0]*math.cos(car.steer+car.rot) - p2f[1]*math.sin(car.steer+car.rot)
        p2s[1] = p2f[0]*math.sin(car.steer+car.rot) + p2f[1]*math.cos(car.steer+car.rot)
        p2s[0] += car.x
        p2s[1] += car.y
        p2s[0] = int((p2s[0] + cam_pos[0])*zoom)
        p2s[1] = int((p2s[1] + cam_pos[1])*zoom)
        p3 = [0, -20]
        p3o = [0, -20]
        p3s = [0, -15]
        p3f = [0, -15]
        p3[0] = p3o[0]*math.cos(car.rot) - p3o[1]*math.sin(car.rot)
        p3[1] = p3o[0]*math.sin(car.rot) + p3o[1]*math.cos(car.rot)
        p3[0] += car.x
        p3[1] += car.y
        p3[0] = int((p3[0] + cam_pos[0])*zoom)
        p3[1] = int((p3[1] + cam_pos[1])*zoom)
        p3s[0] = p3f[0]*math.cos(car.steer+car.rot) - p3f[1]*math.sin(car.steer+car.rot)
        p3s[1] = p3f[0]*math.sin(car.steer+car.rot) + p3f[1]*math.cos(car.steer+car.rot)
        p3s[0] += car.x
        p3s[1] += car.y
        p3s[0] = int((p3s[0] + cam_pos[0])*zoom)
        p3s[1] = int((p3s[1] + cam_pos[1])*zoom)

        pygame.draw.polygon(screen, eval(car.color), [p1, p2, p3])
        pygame.draw.polygon(screen, eval(car.steer_color), [p1s, p2s, p3s])


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
def quit():
    pygame.quit()


if __name__ == "__main__":
    simple_map = [Point("blue", 50, 50), Point("blue", 150, 50), Point("yellow", 50, 120), Point("yellow", 150, 120)]
    simple_lines = [Line(0, 1, "red", 1), Line(0, 2, "green", 2)]
    simple_middleLines = [LineMiddle(0, 2, 0, 1, "blue", 3)]
    simple_cars = [Car(0, 0, math.pi/2, -math.pi/2)]

    init()
    while True:
        draw(simple_map, simple_lines, simple_middleLines, simple_cars)
