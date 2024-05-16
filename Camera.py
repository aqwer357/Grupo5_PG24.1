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

class Camera:
    def __init__(self, pos: Point, target: Point, up: Vector):
        self.pos = pos
        self.target = target
    
        # Vectors of R3
        self.w = pointSubtract(pos, target)
        self.u = cross(self.w, up)
        self.up = up

    def __repr__(self):  # __repr__ is used for debugging
        return f"Camera({self.pos}, {self.target}, {self.up})"

    def __str__(self):  # __str__ is used for printing
        return f"({self.pos}, {self.target}, {self.up})"