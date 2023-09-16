
import pygame
import math
import numpy as np

from init import *
from src import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *

zoom_factor=-5
fov = pi/2


from octrees import *

Scene = getScene()


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

def check_in_bounds(phi, theta, z):
    x_c = z * cos(theta) * sin(phi)
    y_c = z * sin(theta) * sin(phi)
    z_c = z * cos(phi)
    c = np.array([[x_c],
                  [y_c],
                  [z_c]])
    def output(point):
        x, y, z = point
        point = np.array([[x],
                          [y],
                          [z]])
        v = -c
        vnorm = linalg.norm(v)
        vbar = v / vnorm
        d = matmul(point.T, vbar)
        if d >= vnorm:
            return False
        
        cos_theta = d / linalg.norm(x)
        theta = arccos(cos_theta)
        if abs(theta) >= fov / 2:
            return False
        
        return True
    
    return output

def draw_sphere():
    glutSolidSphere(1, 50, 50)


def draw_clickable_points(phi,theta,zoom_factor):
    #points = octree.subset(f_n)
    glDisable(GL_LIGHTING)
    glColor3f(0, 1, 0)  # Green color
    glPointSize(10.0)
    glBegin(GL_POINTS)
    for point,sat in Scene.subset(check_in_bounds(phi,theta,zoom_factor)):
        glVertex3fv(point)
    glEnd()
    glEnable(GL_LIGHTING)





def point_clicked(x, y):
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)
    
    winY = float(viewport[3]) - float(y)
    
    for point, sat in Scene:
        winX, winY, winZ = gluProject(point[0], point[1], point[2], modelview, projection, viewport)
        if abs(winX - x) < 5 and abs(winY - y) < 5:
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
                    if zoom_factor <= 0:
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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(0.0, 0.0, zoom_factor)  # Apply zoom factor here
        glRotatef(math.degrees(theta), 0, 1, 0)
        glRotatef(math.degrees(phi), 1, 0, 0)
        draw_sphere()
        draw_clickable_points(theta,phi,zoom_factor)
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

main()
