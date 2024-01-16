import pygame
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *

fov = (math.pi)/3

# Initialize Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

# Initialize OpenGL
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
glEnable(GL_DEPTH_TEST)
glClearColor(0.5, 0.5, 0.5, 1.0)

# Camera settings
theta = 0
phi = 0
zoom_factor = -5

# Generate some random points for demonstration
np.random.seed(0)
points = np.random.uniform(-10, 10, size=(5000, 3))

def check_in_bounds(phi, theta, z):
    global fov
    # Camera rotation matrix
    R_phi = np.array([
        [1, 0, 0],
        [0, np.cos(phi), -np.sin(phi)],
        [0, np.sin(phi), np.cos(phi)]
    ])
    R_theta = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])
    R = np.dot(R_phi, R_theta)
    
    # Translate along negative z-axis by zoom factor
    T = np.array([0, 0, z])
    
    def output(point):

        # Transform to camera coordinates
        point_cam = np.dot(R, point) + T
        
        # Check if point is behind the camera
        if point_cam[2] > 0:
            return False
        
        # Check if point is within FOV
        x, y, z = point_cam

        
      


        # L = -T  # The camera is at -T, so the line vector is -T
        # print(type(T))
        
        # # Calculate the projection of the point onto the line
        # P_proj = -T + np.dot(point_cam, L) / np.dot(L, L) * L

        # # Check if the projected point is behind the origin
        # if np.linalg.norm(P_proj + T) > np.linalg.norm(L):
        #     return False
        





        angle_x = np.arctan2(np.abs(x), np.abs(z))
        angle_y = np.arctan2(np.abs(y), np.abs(z))
        half_fov = fov / 2.0
        if angle_x > half_fov or angle_y > half_fov:
            return False
        
        return True
    
    return output

# Main loop
dragging = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_drag_origin, y_drag_origin = event.pos
            dragging = True
            if event.button == 4:
                zoom_factor += 0.5
            elif event.button == 5:
                zoom_factor -= 0.5
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        if event.type == pygame.MOUSEMOTION and dragging:
            x, y = event.pos
            dx = x - x_drag_origin
            dy = y - y_drag_origin
            theta += dx * 0.005
            phi += dy * 0.005
            x_drag_origin, y_drag_origin = x, y

    # Clear and draw
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glTranslatef(0.0, 0.0, zoom_factor)
    glRotatef(math.degrees(theta), 0, 1, 0)
    glRotatef(math.degrees(phi), 1, 0, 0)

    # Draw all points
    glDisable(GL_LIGHTING)
    
    glPointSize(10.0)
    glBegin(GL_POINTS)
    for point in points:
        
        if check_in_bounds(phi, theta, zoom_factor)(point):
            glColor3f(0, 1, 0)
            glVertex3fv(point)
        else:
            glColor3f(1, 0, 0)
            glVertex3fv(point)
    glEnd()

    glPopMatrix()
    pygame.display.flip()
    pygame.time.wait(10)