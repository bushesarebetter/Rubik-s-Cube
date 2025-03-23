from math import tan, radians, sin, cos
import numpy as np

def project_points(xyz, WIDTH=800, HEIGHT=600, FOV=45, aspect_ratio=1):
    FOV = radians(FOV)
    if xyz[2] == 0:
        return 0
    bx = xyz[0]/xyz[2] * (1/tan(FOV/2)) * aspect_ratio
    by = xyz[1]/xyz[2] * (1/tan(FOV/2))

    screen_x = int((bx * WIDTH/2) + WIDTH / 2)
    screen_y = int((-by * HEIGHT / 2) + HEIGHT / 2)

    return (screen_x, screen_y)
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
