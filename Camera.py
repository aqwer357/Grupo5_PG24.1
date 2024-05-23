from Elements import Point, Vector, point_subtract, cross

# defines camera and raycasting

class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction.get_normalized()

    def __repr__(self):
        return f"Ray({self.origin}, {self.direction})"

    def __str__(self):
        return f"Ray({self.origin}, {self.direction})"

class Camera:
    def __init__(self, pos: Point, target: Point, up: Vector, dist: float, hScreen: int, wScreen: int):
        self.pos = pos
        self.target = target
        self.w = point_subtract(pos, target).get_normalized()
        self.u = cross(up, self.w).get_normalized()
        self.v = cross(self.w, self.u)
        self.dist = dist
        self.hScreen = hScreen
        self.wScreen = wScreen

    def __repr__(self):
        return f"Camera({self.pos}, {self.target}, {self.dist}, {self.hScreen}, {self.wScreen})"