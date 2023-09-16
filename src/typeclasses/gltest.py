import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Initialize Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Initialize OpenGL
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

vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1],
]

edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
]

faces = [
    (0, 1, 2, 3),
    (3, 7, 6, 2),
    (7, 4, 5, 6),
    (4, 0, 1, 5),
    (1, 5, 6, 2),
    (4, 7, 3, 0),
]

def draw_cube():
    # Enable Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Light Source Properties
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 2, 1, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    
    # Material Properties
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.5, 0.2, 0.2, 1])

    # Draw Faces
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    
    # Disable Lighting for Borders
    glDisable(GL_LIGHTING)
    
    # Draw Borders in Black
    glColor3fv((0, 0, 0))
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    global theta, phi, dragging, x_drag_origin, y_drag_origin

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x_drag_origin, y_drag_origin = event.pos
                dragging = True

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
        glRotatef(math.degrees(theta), 0, 1, 0)
        glRotatef(math.degrees(phi), 1, 0, 0)
        draw_cube()
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
