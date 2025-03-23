from unittest.util import sorted_list_difference
import pygame
import numpy as np
from math import sin, cos, tan, radians, pi
import json


CUBE_DIM = 3 # IMPORTANT


# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

cube_pos = np.array([0, 0, 3000]) # z is distance from cam

faces = [
    (0, 1, 2, 3),  # Front
    (4, 5, 6, 7),  # Back
    (0, 1, 5, 4),  # Bottom
    (2, 3, 7, 6),  # Top
    (0, 3, 7, 4),  # Left
    (1, 2, 6, 5),  # Right
]
# Cube edges
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

COLORES = [
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 255, 255),
    (255, 165, 0),
    (255, 0, 0) 
    ]
                   
 

x_up = []
x_down = []
y_up = []
y_down =[]
z_up = []
z_down = []

def gen_colors(cube_dims: tuple[int, int, int]):
    for _ in range(cube_dims[1]):
        x_up_arr = []
        x_down_arr = []
        for _ in range(cube_dims[2]):
            x_up_arr.append(0)
            x_down_arr.append(1)
        x_up.append(x_up_arr)
        x_down.append(x_down_arr)

        z_up_arr = []
        z_down_arr = []

        for _ in range(cube_dims[0]):
            z_up_arr.append(4)
            z_down_arr.append(5)
        z_up.append(z_up_arr)
        z_down.append(z_down_arr)
    for _ in range(cube_dims[0]):
        y_up_arr = []
        y_down_arr = []
        for _ in range(cube_dims[2]):
            y_up_arr.append(2)
            y_down_arr.append(3)
        y_up.append(y_up_arr)
        y_down.append(y_down_arr)

def check_dir(p):
    current_x, current_y, current_z = (9999, 9999, 9999)
    sum_x = 0
    sum_y = 0
    sum_z = 0
    for point in p:
        if current_x == 9999:
            current_x = point[0]
            current_y = point[1]
            current_z = point[2]
        else:
            if not current_x == -9999:
                if current_x == point[0]:
                    pass
                else:
                    current_x = -9999
            if not current_y == -9999:
                if current_y == point[1]:
                    pass
                else:
                    current_y = -9999
            if not current_z == -9999:
                if current_z == point[2]:
                    pass
                else:
                    current_z = -9999
        sum_x += point[0]
        sum_y += point[1]
        sum_z += point[2]

    if not current_x == -9999:
        average_z = sum_z/800
        average_y = sum_y/800 
        unit_z = int(average_z + cube_z)
        unit_y = int(average_y + cube_y)
        # y is the x, z is the y
        color = x_up[unit_y][unit_z] if current_x > 0 else x_down[unit_y][(CUBE_DIMS[2]-1)-unit_z]
    if not current_y == -9999:
        average_x = sum_x/800
        average_z = sum_z/800 

        unit_x = int(average_x + cube_x)
        unit_z = int(average_z + cube_z)

        # y is the x, z is the y
        color = y_up[unit_x][unit_z] if current_y > 0 else y_down[(CUBE_DIMS[2]-1)-unit_z][unit_x]
    if not current_z == -9999:
        average_x = sum_x/800
        average_y = sum_y/800 
        unit_x = int(average_x + cube_x)
        unit_y = int(average_y + cube_y)
        # y is the x, z is the y
        color = z_up[(CUBE_DIMS[1]-1)-unit_y][unit_x] if current_z > 0 else z_down[unit_y][unit_x]
    return color

def create_cubes(CUBE_DIMS=(3,3,3)):

    OFFSET_X = -cube_x
    OFFSET_Y = -cube_y
    OFFSET_Z = -cube_z
    cube_positions = []
    counter_x = 0
    counter_y = 0
    counter_z = 0
    for z in range(CUBE_DIMS[2]):
        for y in range(CUBE_DIMS[1]):
            for x in range(CUBE_DIMS[0]):
                cube_positions.append([OFFSET_X + counter_x, OFFSET_Y + counter_y, OFFSET_Z + counter_z])
                counter_x += 1
                counter_x = counter_x % CUBE_DIMS[0]
            counter_y += 1
            counter_y = counter_y % CUBE_DIMS[1]
        counter_z += 1
    


    

    cubes= []
    for t in cube_positions:
        cube = np.array([
            [-1 + t[0] * 2, -1 + t[1] *2, -1 + t[2] * 2],
            [1 + t[0] * 2, -1 + t[1] *2, -1 + t[2] * 2],
            [1 + t[0] * 2, 1 + t[1] *2, -1 + t[2] * 2],
            [-1 + t[0] * 2, 1 + t[1] *2, -1 + t[2] * 2],
            [-1 + t[0] * 2, -1 + t[1] *2, 1 + t[2] * 2],
            [1 + t[0] * 2, -1 + t[1] *2, 1 + t[2] * 2],
            [1 + t[0] * 2, 1 + t[1] *2, 1 + t[2] * 2],
            [-1 + t[0] * 2, 1 + t[1] *2, 1 + t[2] * 2],
        ]) * 100
        cubes.append(cube)
    return cubes
        
def transform_point(point, rot_x, rot_y, rot_z, position):
    point.reshape(3,1)
    transform1 = np.array([[1, 0, 0],
                           [0, cos(rot_x), -sin(rot_x)],
                           [0, sin(rot_x), cos(rot_x)]])
    transform2 = np.array([[cos(rot_y), 0, -sin(rot_y)],
                          [0, 1, 0],
                          [sin(rot_y), 0, cos(rot_y)]])
    transform3 = np.array([[cos(rot_z), -sin(rot_z), 0],
                           [sin(rot_z), cos(rot_z), 0],
                           [0, 0, 1]])
    
    full_transform = np.dot(np.dot(transform1, transform2), transform3)

    transformed_point = np.dot(full_transform, point)
    transformed_point += position

    return transformed_point.flatten()

def project_points(xyz, FOV=45, aspect_ratio=1):
    FOV = radians(FOV)
    if xyz[2] == 0:
        return 0
    bx = xyz[0]/xyz[2] * (1/tan(FOV/2)) * aspect_ratio
    by = xyz[1]/xyz[2] * (1/tan(FOV/2))

    screen_x = int((bx * WIDTH/2) + WIDTH / 2)
    screen_y = int((-by * HEIGHT / 2) + HEIGHT / 2)

    return (screen_x, screen_y)

def accumulate_faces(cubes, faces=faces):
    accumulated_faces = []
    face_hashmap = {}
    for cube in cubes:
        transformed_vertices = cube #looks like we transform before assinging and then transforming
        for face in faces:
            face_points = [transformed_vertices[face[n]] for n in range(4)]
            sorted_points = sorted([tuple(np.round(point, 6)) for point in face_points])
            face_hash = str(sorted_points)
            if face_hash in face_hashmap:
                face_hashmap[face_hash].append((face_points, check_dir(face_points)))
            else:
                face_hashmap[face_hash] = [(face_points, check_dir(face_points))]
    for face_hash, face_list in face_hashmap.items():
        if len(face_list) == 1:
            accumulated_faces.append((face_list[0][0], face_list[0][1]))
    
    return accumulated_faces

def sort_faces(accumulated_faces):
    average_z_value = []
    faces_with_colors = []
    for face, color in accumulated_faces:
        transformed_points = [transform_point(face[n], rot_x, rot_y, rot_z, cube_pos) for n in range(4)]

        faces_with_colors.append((transformed_points, color))

        sum_z = sum(point[2] for point in transformed_points)
        average_z_value.append(sum_z/4)
    
    paired = list(zip(average_z_value, faces_with_colors))
    paired.sort(reverse=True, key=lambda x: x[0])
    if not paired:
        return []
    _, sorted_faces_with_colors = zip(*paired)
    return list(sorted_faces_with_colors)


running = True

CUBE_DIMS = (3, 3, 3)
cube_x = (CUBE_DIMS[0] - 1)/2
cube_y = (CUBE_DIMS[1] - 1)/2
cube_z = (CUBE_DIMS[2] - 1)/2
cubes = create_cubes(CUBE_DIMS)
gen_colors(CUBE_DIMS)
accumulated_faces = accumulate_faces(cubes) # yay optimized :D


rot_x = 0
rot_y = 0
rot_z = 0
vel = 0.05
while running:

    clock.tick(60)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        rot_y += vel
    elif keys[pygame.K_LEFT]:
        rot_y -= vel
    if keys[pygame.K_UP]:
        rot_x += vel
    elif keys[pygame.K_DOWN]:
        rot_x -= vel
    
    if abs(rot_x) > 2 * pi:
        rot_x = 0
    if abs(rot_y) > 2 * pi:
        rot_y = 0
        
    screen.fill((0, 0, 0))

    sorted_faces = sort_faces(accumulated_faces)

    for face, color in sorted_faces:
        # projecting once and accessing twice is better than projecting twice??

        projected_points = [project_points(face[n]) for n in range(4)]
        pygame.draw.polygon(screen, COLORES[color], [(projected_points[n]) for n in range(4)])
        
        for pair_index in range(len(projected_points)-1):
          pygame.draw.line(screen, (0, 0, 0), projected_points[pair_index], projected_points[pair_index+1], 5)
        # take face coords (projected), draw lines
        # any way to just draw outline around the faces? seeing as its already sorted and transformed
        
    pygame.display.flip()

pygame.quit()

