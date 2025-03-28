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


                   
 

face_colors = [
    [],
    [],
    [],
    [],
    [],
    []
]

def gen_colors(cube_dims: tuple[int, int, int]):
    for _ in range(cube_dims[1]):
        x_up_arr = []
        x_down_arr = []
        for _ in range(cube_dims[2]):
            x_up_arr.append(0)
            x_down_arr.append(1)
        face_colors[0].append(x_up_arr)
        face_colors[1].append(x_down_arr)

        z_up_arr = []
        z_down_arr = []

        for _ in range(cube_dims[0]):
            z_up_arr.append(4)
            z_down_arr.append(5)
        face_colors[4].append(z_up_arr)
        face_colors[5].append(z_down_arr)
    for _ in range(cube_dims[0]):
        y_up_arr = []
        y_down_arr = []
        for _ in range(cube_dims[2]):
            y_up_arr.append(2)
            y_down_arr.append(3)
        face_colors[2].append(y_up_arr)
        face_colors[3].append(y_down_arr)

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
        # y is the y, z is the x
        index, face_side = ((unit_z, CUBE_DIM-1-unit_y), 0) if current_x > 0 else ((unit_z, unit_y), 1)
    if not current_y == -9999:
        average_x = sum_x/800
        average_z = sum_z/800 

        unit_x = int(average_x + cube_x)
        unit_z = int(average_z + cube_z)

        # y is the x, z is the y
        index, face_side = ((unit_z, unit_x), 2) if current_y > 0 else ((unit_z, CUBE_DIM-1-unit_x), 3)
    if not current_z == -9999:
        average_x = sum_x/800
        average_y = sum_y/800 
        unit_x = int(average_x + cube_x)
        unit_y = int(average_y + cube_y)
        # y is the x, z is the y
        index, face_side = ((CUBE_DIM-1-unit_y, CUBE_DIM-1-unit_x), 4) if current_z > 0 else ((unit_y, CUBE_DIM-1-unit_x), 5)

    return index, face_side

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
def find_associated(idx):
    match idx:
        case 0:
            return ((5, 1, 0, 0), (2, 1, CUBE_DIM-1, 0), (4, 1, 0, 0), (3, 1, 0, 1), False)
        case 1:
            return ((4, 1, CUBE_DIM-1, 0), (2, 1, 0, 0), (5, 1, CUBE_DIM-1, 0), (3, 1, CUBE_DIM-1, 1), False)
        case 2:
            return ((5, 0, CUBE_DIM-1, 0), (0, 1, 0, 1), (4, 0, 0, 1), (1, 1, CUBE_DIM-1, 0), True)
        case 3:
            return ((1, 1, 0, 1), (5, 0, 0, 1), (0, 1, CUBE_DIM-1, 0), (4, 0, CUBE_DIM-1, 0), False)
        case 4:
            return ((0, 0, CUBE_DIM-1, 0), (2, 0, CUBE_DIM-1, 0), (1, 0, CUBE_DIM-1, 0), (3, 0, CUBE_DIM-1, 0), True)
        case 5:
            return ((1, 0, 0, 0), (2, 0, 0, 0), (0, 0, 0, 0), (3, 0, 0, 0), True)
def shift_columns(faces, direction='up'): # if col is 1 then extract col, if col is 0 then extract row
    cols = []
    for face, col, col_idx, reverse in faces:
        face = face_colors[face]
        if col == 1:
            if reverse:
                for row in reversed(face):
                    cols.append(row[col_idx])
            else:
                for row in face:
                    cols.append(row[col_idx])   
        else:
            if reverse:
                for item in reversed(face[col_idx]):
                    cols.append(item)
            else:
                for item in face[col_idx]:
                    cols.append(item)
    if direction == 'up':
        for _ in range(CUBE_DIM):
            cols.append(cols.pop(0)) 
    elif direction == 'down':
        for _ in range(CUBE_DIM):
            cols.insert(0, cols.pop())
    i = 0
    for face, col, col_idx, reverse in faces:
        face = face_colors[face]
        if col == 1:
            if reverse:
                for row in reversed(face):
                    row[col_idx] = cols[i]
                    i+= 1
            else:    
                for row in face:
                    row[col_idx] = cols[i]
                    i+= 1
        else:
            if reverse:
                for j in reversed(range(len(face[col_idx]))):
                    face[col_idx][j] = cols[i]
                    i+= 1
            else:
                for j in range(len(face[col_idx])):
                    face[col_idx][j] = cols[i]
                    i+= 1
            


    # we collect rows, columns, whatever, then we shift, then we look at each face and change each row/column

def rotate(matrix_2d_idx, clockwise=True, assigned_idx=False):
    matrix_2d = face_colors[matrix_2d_idx]
    faces = find_associated(matrix_2d_idx)
    if assigned_idx:
        #this is going to be painful
        tuple_1 = faces[0]
        tuple_2 = faces[1]
        tuple_3 = faces[2]
        tuple_4 = faces[3]
        faces = ((tuple_1[0], tuple_1[1], 1, tuple_1[3]), 
                     (tuple_2[0], tuple_2[1], 1, tuple_2[3]),
                     (tuple_3[0], tuple_3[1], 1, tuple_3[3]),
                     (tuple_4[0], tuple_4[1], 1, tuple_4[3]),
                     faces[4]
        )
    else:
        if clockwise:
            if faces[4]:
                matrix_2d[:] = [list(row) for row in zip(*matrix_2d)]
                n = len(matrix_2d)
                for j in range(n):
                    for i in range(n // 2):
                        matrix_2d[i][j], matrix_2d[n - 1 - i][j] = matrix_2d[n - 1 - i][j], matrix_2d[i][j]
            else:
                n = len(matrix_2d)
                for i in range(n):
                    for j in range(i+1, n):
                        matrix_2d[i][j], matrix_2d[j][i] = matrix_2d[j][i], matrix_2d[i][j]
                for row in matrix_2d:
                    row.reverse()

        else:
            if faces[4]:
                n = len(matrix_2d)
                for i in range(n):
                    for j in range(i+1, n):
                        matrix_2d[i][j], matrix_2d[j][i] = matrix_2d[j][i], matrix_2d[i][j]
                for row in matrix_2d:
                    row.reverse()
            
            else:
                matrix_2d[:] = [list(row) for row in zip(*matrix_2d)]
                n = len(matrix_2d)
                for j in range(n):
                    for i in range(n // 2):
                        matrix_2d[i][j], matrix_2d[n - 1 - i][j] = matrix_2d[n - 1 - i][j], matrix_2d[i][j]

    shift_columns([(faces[n][0], faces[n][1], faces[n][2], faces[n][3]) for n in range(4)], 'up' if clockwise else 'down')
def assign_moves(curr_face):
    match curr_face:
        case 5:
            return (5, 4, 1, 0, 0)
        case 4:
            return (4, 5, 0, 1, pi)
        case 1:
            return (1, 0, 4, 5, pi/2)
        case 0:
            return (0, 1, 5, 4, -pi/2)

COLORES = [
    (0, 255, 0), # green
    (0, 0, 255), # blue
    (255, 255, 0), # yellow
    (255, 255, 255), # white
    (255, 165, 0), # orange
    (255, 0, 0) # red
]


running = True

CUBE_DIMS = (CUBE_DIM, CUBE_DIM, CUBE_DIM)
cube_x = (CUBE_DIMS[0] - 1)/2
cube_y = (CUBE_DIMS[1] - 1)/2
cube_z = (CUBE_DIMS[2] - 1)/2
cubes = create_cubes(CUBE_DIMS)
gen_colors(CUBE_DIMS)

accumulated_faces = accumulate_faces(cubes) # yay optimized :D





rot_x = -pi/10
rot_y = 0
rot_z = 0
vel = 0.05
flag = False
front_face = 0
x_faces = (5, 0, 4, 1)
assigned_moves = assign_moves(x_faces[front_face])

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
    if flag==False:   
        if keys[pygame.K_f]: # red will always 'face' front
            starttime = pygame.time.get_ticks()
            flag = True
            rotate(assigned_moves[0], keys[pygame.K_LSHIFT])
            if keys[pygame.K_1]:
                rotate(assigned_moves[0], keys[pygame.K_LSHIFT], True)

        if keys[pygame.K_b]:
            starttime = pygame.time.get_ticks()
            flag = True
            rotate(assigned_moves[1], keys[pygame.K_LSHIFT])
            if keys[pygame.K_1]:
                rotate(assigned_moves[1], keys[pygame.K_LSHIFT], True)
        if keys[pygame.K_l]:
            starttime = pygame.time.get_ticks()
            flag = True
            rotate(assigned_moves[2], keys[pygame.K_LSHIFT])
            if keys[pygame.K_1]:
                rotate(assigned_moves[2], keys[pygame.K_LSHIFT], True)
        if keys[pygame.K_r]:
            starttime = pygame.time.get_ticks()
            flag = True
            rotate(assigned_moves[3],  keys[pygame.K_LSHIFT])
            if keys[pygame.K_1]:
                rotate(assigned_moves[3], keys[pygame.K_LSHIFT], True)
        if keys[pygame.K_m]:
            starttime = pygame.time.get_ticks()
            flag = True
            rotate(assigned_moves[2], keys[pygame.K_LSHIFT], True)
        if keys[pygame.K_u]:
            starttime = pygame.time.get_ticks()
            flag = True
            rotate(2, not keys[pygame.K_LSHIFT])
            if keys[pygame.K_1]:
                rotate(2, not keys[pygame.K_LSHIFT], True)
        if keys[pygame.K_d]:
            starttime = pygame.time.get_ticks()
            flag = True
            rotate(3, keys[pygame.K_LSHIFT])
            if keys[pygame.K_1]:
                rotate(3, keys[pygame.K_LSHIFT], True)
        
        if keys[pygame.K_x]:
            starttime = pygame.time.get_ticks()
            flag = True
            
            front_face += -1 if keys[pygame.K_LSHIFT] else 1
            if front_face == len(x_faces):
                front_face = 0
            if front_face < 0:
                front_face = len(x_faces)-1

            assigned_moves = assign_moves(x_faces[front_face])
            rot_y = assigned_moves[4]
            
            rot_x=-pi/10




    if abs(rot_x) > 2*pi:
        rot_x = 0
    if abs(rot_y) > 2*pi:
        rot_y = 0
    if flag==True and pygame.time.get_ticks() - starttime > 200:
        flag = False
    screen.fill((0, 0, 0))

    sorted_faces = sort_faces(accumulated_faces)

    for face, color in sorted_faces:
        # projecting once and accessing twice is better than projecting twice??
        # color[0] has index to pull from
        # color[1] has array details 
        projected_points = [project_points(face[n]) for n in range(4)]
        pygame.draw.polygon(screen, COLORES[face_colors[color[1]][color[0][0]][color[0][1]]], [(projected_points[n]) for n in range(4)])
        
        for pair_index in range(len(projected_points)-1):
          
          pygame.draw.line(screen, (0, 0, 0), projected_points[pair_index], projected_points[pair_index+1], 5)
        # take face coords (projected), draw lines
        # any way to just draw outline around the faces? seeing as its already sorted and transformed
        
    pygame.display.flip()

pygame.quit()

