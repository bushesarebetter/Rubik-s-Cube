import numpy as np
from directional import Directional
from stuff3d import transform_point
class RubiksCube:

    faces = [
    (0, 1, 2, 3),  # Front
    (4, 5, 6, 7),  # Back
    (0, 1, 5, 4),  # Bottom
    (2, 3, 7, 6),  # Top
    (0, 3, 7, 4),  # Left
    (1, 2, 6, 5),  # Right
    ]

    rot_x = 0
    rot_y = 0
    rot_z = 0
    cube_pos = np.array([0, 0, 3000])

    def __init__(self, dim: int, window_dims: tuple[int, int]):
        # create cubes with dims
        # handle face accumulation DURING INIT
        # face sorting during loop, we could make a loop call 
        self.dim = dim
        self.cube_offset = (dim - 1) / 2
        self.create_cubes(100)
        print('Created cubes!')
        self.directional = Directional()
        self.directional.fill_colors(dim) # at this point we have everything until the main loop implemented
        print('Created faces/colors')
        self.accumulate_faces() # create self.accumulated faces, not transformed YET
        print('Accumulated faces!')
    def sort_faces(self):
        # assumes accumulated faces, NOW we transform and sort (yay)
        average_z_val = []
        faces_with_colors = []

        for face, color in self.accumulated_faces:
            transformed_face = [transform_point(p, self.rot_x, self.rot_y, self.rot_z, self.cube_pos) for p in face] # only transform during the loop so we can keep accumulated faces outside 
            faces_with_colors.append((transformed_face, color))
            sum_z = sum(point[2] for point in transformed_face)
            average_z_val.append(sum_z/4)
        
        paired = list(zip(average_z_val, faces_with_colors))
        paired.sort(reverse=True, key=lambda x: x[0])
        if not paired:
            return []
        _, self.sorted_faces = zip(*paired)
        return self.sorted_faces #optional
    # so theoretically i should be able to run this and it wont break........... rightttt????

    def create_cubes(self, cube_size: int):
        temp_cube_offset = -self.cube_offset

        cube_positions = [
            [temp_cube_offset + x, temp_cube_offset + y, temp_cube_offset + z]
            for z in range(self.dim)
            for y in range(self.dim)
            for x in range(self.dim)
        ]

        self.cubes = [
            np.array([
                [-1 + x * 2, -1 + y * 2, -1 + z * 2],
                [1 + x * 2, -1 + y * 2, -1 + z * 2],
                [1 + x * 2, 1 + y * 2, -1 + z * 2],
                [-1 + x * 2, 1 + y * 2, -1 + z * 2],
                [-1 + x * 2, -1 + y * 2, 1 + z * 2],
                [1 + x * 2, -1 + y * 2, 1 + z * 2],
                [1 + x * 2, 1 + y * 2, 1 + z * 2],
                [-1 + x * 2, 1 + y * 2, 1 + z * 2],
            ]) * cube_size
            for x, y, z in cube_positions
        ]
    def check_dir(self, face_points): # i forgor the type
        current_x = current_y = current_z = 9999
        sum_x = sum_y = sum_z = 0

        for point in face_points:
            if current_x == 9999:
                current_x = point[0]
                current_y = point[1]
                current_z = point[2]
            else:
                if not (current_x == -9999 or current_x == point[0]):
                    current_x = -9999
                if not (current_y == -9999 or current_y == point[1]):
                    current_y = -9999
                if not (current_z == -9999 or current_z == point[2]):
                    current_z = -9999
            sum_x += point[0]
            sum_y += point[1]
            sum_z += point[2]

        average_x = sum_x/800
        average_y = sum_y/800
        average_z = sum_z/800
        unit_x = int(average_x + self.cube_offset)
        unit_y = int(average_y + self.cube_offset)
        unit_z = int(average_z + self.cube_offset)

        if not current_x == -9999: 
            color = self.directional.x_up[unit_y][unit_z] if current_x > 0 else self.directional.x_down[unit_y][(self.dim -1) - unit_z]
        elif not current_y == -9999:
            color = self.directional.y_up[unit_x][unit_z] if current_y > 0 else self.directional.y_down[(self.dim - 1) - unit_z][unit_x]
        elif not current_z == -9999:
            color = self.directional.z_up[(self.dim-1)-unit_y][unit_x] if current_z > 0 else self.directional.z_down[unit_y][unit_x]

        return color

        
    def accumulate_faces(self):
        self.accumulated_faces = []
        face_hashmap = {}
        for cube in self.cubes:
            for face in self.faces:
                face_points = [cube[face[n]] for n in range(4)]
                sorted_points = sorted([tuple(np.round(point, 6)) for point in face_points])
                face_hash = str(sorted_points)
                if face_hash in face_hashmap:
                    face_hashmap[face_hash].append((face_points, self.check_dir(face_points)))
                else:
                    face_hashmap[face_hash] = [(face_points, self.check_dir(face_points))]
            
            for face_hash, face_list in face_hashmap.items():
                if len(face_list) == 1:
                    self.accumulated_faces.append((face_list[0][0], face_list[0][1]))
    
            




