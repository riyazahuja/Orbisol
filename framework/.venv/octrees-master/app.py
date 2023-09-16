
import pygame
from init import *
from src import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
import math

zoom_factor=-5


from octrees import *

Scene = getScene()
NumScenes = 1

if Scene is None:
    raise Exception('Scene not initialized')

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
# Additional OpenGL settings
glEnable(GL_DEPTH_TEST)
glClearColor(0.5, 0.5, 0.5, 1.0)
# Mouse control variables
dragging = False
x_drag_origin = 0
y_drag_origin = 0
theta = 0
phi = 0
# Points list
#points = [(0, 2, 1), (1, 0, 2), (1, 0, 0), (2, 0, 0), (2, 0, 0)]
#octree = Octree(((-100, 100), (-100, 100), (-100, 100)))

def increment_speed():
    delta_time_scale = Satellite.delta_time_scale
    if Satellite.time_scale < 0.00005:
        Satellite.time_scale += delta_time_scale

def decrement_speed():
    delta_time_scale = Satellite.delta_time_scale
    if Satellite.time_scale > -0.00005:
        Satellite.time_scale -= delta_time_scale


def update_scene():
    global NumScenes
    NumScenes += 1
    ts = Satellite.get_timescale()
    now = ts.now()
    t_scaled = now + NumScenes * Satellite.time_scale
    
    for prev_pos, satellite in Scene:
        new_pos = satellite.get_pos(t_scaled)
        try:
            Scene.remove(prev_pos)
        except:
            pass
        Scene.update(new_pos, satellite)

def draw_sphere():
    glutSolidSphere(1, 50, 50)


def draw_clickable_points():
    #points = octree.subset(f_n)
    glDisable(GL_LIGHTING)
    glColor3f(0, 1, 0)  # Green color
    glPointSize(10.0)
    glBegin(GL_POINTS)
    for point,sat in Scene:
        glVertex3fv(point)
    glEnd()
    glEnable(GL_LIGHTING)
def point_clicked(x, y):
    for point,sat in Scene:
        px, py, pz = point
        # Convert to screen coordinates
        # ... (conversion logic, if needed)
        # Check if clicked
        # ... (check logic)
        # For demonstration, just print the point if clicked
        print(f"Point clicked: {point} | Sat: {sat.name}")
def main():
    global theta, phi, dragging, x_drag_origin, y_drag_origin,zoom_factor
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_drag_origin, y_drag_origin = event.pos
                dragging = True
                point_clicked(*event.pos)  # Check for point clicks

                if event.button == 4:  # Scroll up
                    zoom_factor += 0.5  # Increase the zoom factor
                elif event.button == 5:  # Scroll down
                    zoom_factor -= 0.5  # Decrease the zoom factor

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            if event.type == pygame.MOUSEMOTION and dragging:
                x, y = event.pos
                dx = x - x_drag_origin
                dy = y - y_drag_origin
                theta += dx * 0.005
                phi += dy * 0.005
                x_drag_origin, y_drag_origin = x, y
            keys = pygame.key.get_pressed()
            if K_UP in keys:
                increment_speed()
            elif K_DOWN in keys:
                decrement_speed()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(0.0, 0.0, zoom_factor)  # Apply zoom factor here
        glRotatef(math.degrees(theta), 0, 1, 0)
        glRotatef(math.degrees(phi), 1, 0, 0)
        draw_sphere()
        draw_clickable_points()
        glPopMatrix()
        update_scene()
        pygame.display.flip()
        pygame.time.wait(10)

main()












