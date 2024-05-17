import math
from Elements import Point, Vector

def pointSubtract(p1: Point, p2: Point):
    v = Vector(0,0,0)

    v.x = p1.x - p2.x
    v.y = p1.y - p2.y
    v.z = p1.z - p2.z

    return v
def cross(v1: Vector, v2: Vector):
    product = Vector(v1.y*v2.z - v2.z*v2.y,
                     v1.z*v2.x - v2.x*v2.z,
                     v1.x*v2.y - v2.y*v2.x,)
    return product


def pointDistance(p1: Point, p2: Point):

    difference = math.pow((p1.x - p2.x), 2) + math.pow((p1.y - p2.y), 2) + math.pow((p1.z - p2.z), 2)

    distance = math.sqrt(difference)

    return round(distance, 2)

class Camera:
    def __init__(self, pos: Point, target: Point, up: Vector, screen_width: int, screen_height: int):
        self.pos = pos
        self.target = target
    
        # Vectors of R3
        self.w = pointSubtract(pos, target)
        self.u = cross(self.w, up)
        self.v = cross(self.w, self.u)
        self.up = up

        # Screen Dimensions

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Distance from camera to screen

        self.distance = pointDistance(pos, target)


    def rayCast():
        return 0
    

    def __repr__(self):  # __repr__ is used for debugging
        return f"Camera({self.pos}, {self.target}, {self.up})"

    def __str__(self):  # __str__ is used for printing
        return f"({self.pos}, {self.target}, {self.up})"
    
