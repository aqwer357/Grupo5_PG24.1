import math

def affine_transform(pointOrVector, transform_type="", x=0, y=0, z=0, angle=0):
    if transform_type == 'translate':
        matrix = translate(x, y, z)
    elif transform_type == 'scale':
        matrix = scale(x, y, z)
    elif transform_type == 'rotate_x':
        matrix = rotate_x(angle)
    elif transform_type == 'rotate_y':
        matrix = rotate_y(angle)
    elif transform_type == 'rotate_z':
        matrix = rotate_z(angle)
    else:
        print ("Transform type not supported")

    result = dotProd_matrixTuple(matrix, pointOrVector)

    return result

# translation matrix
def translate(x, y, z):
    matrix = [[1, 0, 0, x],
              [0, 1, 0, y],
              [0, 0, 1, z],
              [0, 0, 0, 1]]
    return matrix

# scale matrix
def scale(x, y, z):
    matrix = [[x, 0, 0, 0],
              [0, y, 0, 0],
              [0, 0, z, 0],
              [0, 0, 0, 1]]
    return matrix

# rotation matrices
def rotate_x(angle):
    matrix = [[1, 0, 0, 0],
              [0, math.cos(angle), -math.sin(angle), 0],
              [0, math.sin(angle),  math.cos(angle), 0],
              [0, 0, 0, 1]]
    return matrix

def rotate_y(angle):
    matrix = [[ math.cos(angle), 0, math.sin(angle), 0],
              [0, 1, 0, 0],
              [-math.sin(angle), 0, math.cos(angle), 0],
              [0, 0, 0, 1]]
    return matrix

def rotate_z(angle):
    matrix = [[math.cos(angle), -math.sin(angle), 0, 0],
              [math.sin(angle),  math.cos(angle), 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]]
    return matrix

# WIP, actual calculation of matrix * vector/point
def dotProd_matrixTuple(matrix, pointOrVector):
    x=0
    y=0
    z=0
    return [x,y,z]