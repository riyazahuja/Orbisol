import pygame
import math
import numpy as np

from init import *
from data import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *

import math
import numpy as np



#from octrees import *

zoom_factor=-5
fov = math.pi
Scene = getScene()
info_panel = False
clicked_sat = None

TimeAhead = 0


if Scene is None:
    raise Exception('Scene not initialized')

# Initialize Pygame and OpenGL
pygame.init()
display = (1500, 900)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
# Additional OpenGL settings
glEnable(GL_DEPTH_TEST)
#glClearColor(0.5, 0.5, 0.5, 1.0)
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
    if Satellite.time_scale < 0.0003:
        Satellite.time_scale += delta_time_scale

def decrement_speed():
    delta_time_scale = Satellite.delta_time_scale
    if Satellite.time_scale > -0.0003:
        Satellite.time_scale -= delta_time_scale


def update_scene():
    global TimeAhead
    TimeAhead += 1 * Satellite.time_scale
    ts = Satellite.get_timescale()
    now = ts.now()
    t_scaled = now + TimeAhead
    
    for prev_pos, satellite in Scene:
        new_pos = satellite.get_pos(t_scaled)
        try:
            Scene.remove(prev_pos)
        except:
            pass
        Scene.update(new_pos, satellite)


def draw_sphere():
    glDisable(GL_LIGHTING)
    glColor3f(0.0, 0.0, 1.0)  # RGB for blue
    glutSolidSphere(1, 50, 50)
    glEnable(GL_LIGHTING)



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
        return True

        # Transform to camera coordinates
        point_cam = np.dot(R, point) + T
        
        # Check if point is behind the camera
        if point_cam[2] > 0:
            return False
        
        # Check if point is within FOV
        x, y, z = point_cam

        
      


        # L = -T  # The camera is at -T, so the line vector is -T
        # # print(type(T))
        
        # # # Calculate the projection of the point onto the line
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


def draw_clickable_points(phi,theta,z):
    
    #points = octree.subset(f_n)
    glDisable(GL_LIGHTING)
   
    glPointSize(3.0)
    glBegin(GL_POINTS)

    for point,sat in Scene:
        if check_in_bounds(phi,theta,z)(point):
            if sat.type == 'active':
                glColor3f(0, 1, 0)  # Green color
                glVertex3fv(point)
            elif sat.type == 'inactive':
                glColor3f(1, 0, 0)  # Red color
                glVertex3fv(point)
            else:
                glColor3f(1, 0, 1)  # Green color
                glVertex3fv(point)
    glEnd()
    glEnable(GL_LIGHTING)


    

def point_clicked(x, y):
    global info_panel, clicked_sat
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)
    
    winY = float(viewport[3]) - float(y)
    
    for point, sat in Scene:
        winX, winY, winZ = gluProject(point[0], point[1], point[2], modelview, projection, viewport)
        if abs(winX - x) <30 and abs(winY - y) < 30:
            print(f"Point clicked: {point} | Sat: {sat.name}")
            info_panel = True
            clicked_sat = sat
            print('Yahoo')

def draw_text(x, y, text, font, color=(255, 255, 255)):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glDisable(GL_BLEND)


def get_orbital_data(sat):
    # Initialize the satellite object
    sat = sat.satellite#EarthSatellite(sat.TLE[0], sat.TLE[1], sat.name, Satellite.get_timescale())

    # Fetch the orbital parameters
    model = sat.model  # This holds the SGP4 model data
    i = model.inclo
    raan = model.nodeo  # Right Ascension of Ascending Node
    e = model.ecco
    argp = model.argpo  # Argument of Perigee
    M = model.mo  # Mean Anomaly
    n = model.no_kozai  # Mean Motion

    # Convert radians to degrees for easier interpretation
    i_deg = np.degrees(i)
    raan_deg = np.degrees(raan)
    argp_deg = np.degrees(argp)
    M_deg = np.degrees(M)

    # Create a dictionary to store the data
    orbital_data = {
        'Inclination (deg)': i_deg,
        'RAAN (deg)': raan_deg,
        'Eccentricity': e,
        'Argument of Perigee (deg)': argp_deg,
        'Mean Anomaly (deg)': M_deg,
        'Mean Motion (rev/day)': n * 60 / (2 * np.pi),  # convert to rev/day
    }
    
    return orbital_data

def draw_info_panel():
    if not info_panel or clicked_sat is None:
        return

    data = get_orbital_data(clicked_sat)


    # Save current matrices
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Disable 3D-specific settings
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)

    # Switch to 2D
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, display[0], 0, display[1])

    # Draw the rectangle (make it white)
    glColor3f(0, 0, 0)  # White
    glBegin(GL_QUADS)
    glVertex2f(0,0)
    glVertex2f(1500, 0)
    glVertex2f(1500, 200)
    glVertex2f(0, 200)
    glEnd()

    # Draw the text (make it black)
    font = pygame.font.Font(None, 36)
    font2 = pygame.font.Font(None, 24)
    
    draw_text(60, 150, f"Satellite: {clicked_sat.name}", font, color=(255, 255, 255))
    curr = 120
    x=60
    for k,v in data.items():
        draw_text(x, curr, f"{k}: {v}", font2, color=(255, 255, 255))
        curr=curr-20
        if curr<75:
            curr = 120
            x += 500
    
    draw_text(1100,120,f"Status: {clicked_sat.type}" ,font2, color = (255,255,255))

    draw_text(1100,80,f"Time Scale: {Satellite.time_scale}" ,font2, color = (255,255,255))

    # Restore previous settings and matrices
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()




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
                theta += dx * 0.03#0.005
                phi += dy * 0.03#0.005
                x_drag_origin, y_drag_origin = x, y
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    increment_speed()
                elif event.key == pygame.K_DOWN:
                    decrement_speed()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(0.0, 0.0, zoom_factor)  # Apply zoom factor here
        glRotatef(theta, 0, 1, 0)
        glRotatef(phi, 1, 0, 0)
        draw_sphere()

        draw_clickable_points(phi,theta,zoom_factor)

        glPopMatrix()
        update_scene()

        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)

        # Draw panel here
        draw_info_panel()
        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        
        pygame.display.flip()
        pygame.time.wait(10)

main()
