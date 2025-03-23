from rubikscube import RubiksCube
import pygame
from math import pi
from stuff3d import project_points
from colors import COLORS

pygame.init()
WIDTH = 800
HEIGHT = 600
VEL = 0.1
cube = RubiksCube(3, (WIDTH, HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

while running:
    clock.tick(120)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        cube.rot_y += VEL
    elif keys[pygame.K_LEFT]:
        cube.rot_y -= VEL
    if keys[pygame.K_UP]:
        cube.rot_x += VEL
    elif keys[pygame.K_DOWN]:
        cube.rot_x -= VEL
    
    if abs(cube.rot_x) > 2 * pi:
        rot_x = 0
    if abs(cube.rot_y) > 2 * pi:
        rot_y = 0

    screen.fill((0, 0, 0))

    # WE already have the accumulated faces, now we can just sort them
    cube.sort_faces()

    for face, color in cube.sorted_faces:

        pygame.draw.polygon(screen, COLORS.COLORES[color], [(project_points(face[n])[0], project_points(face[n])[1]) for n in range(4)])
    
    pygame.display.flip()
    
