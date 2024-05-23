# defines elements of R3

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def get_magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def get_normalized(self):
        magnitude = self.get_magnitude()
        if magnitude == 0:
            return Vector(0, 0, 0)
        return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)


class Sphere:
    def __init__(self, center: Point, radius: float, colorRGB: Vector):
        self.center = center
        self.radius = radius
        self.colorRGB = colorRGB

    def __repr__(self):
        return f"Sphere({self.center}, {self.radius}, {self.colorRGB})"

    class IntersectOutput:
        def __init__(self, intersectPoint: Point, t):
            self.intersectPoint = intersectPoint
            self.t = t

    def intersect(self, origin: Point, direction: Vector):
        oc = point_subtract(origin, self.center)
        a = direction.x**2 + direction.y**2 + direction.z**2
        b = 2.0 * (oc.x * direction.x + oc.y * direction.y + oc.z * direction.z)
        c = oc.x**2 + oc.y**2 + oc.z**2 - self.radius**2
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            # if discriminant < 0 -> no intersection
            return None
        else:
            # we choose negative in quadratic formula to choose the first point of intersection with the sphere
            t = (-b - discriminant**0.5) / (2.0 * a)
            if t >= 0:
                intersect_point = self.IntersectOutput(Point(origin.x + t * direction.x,
                                                             origin.y + t * direction.y,
                                                             origin.z + t * direction.z),
                                                             t)
                return intersect_point
            else:
                # t <= 0 --> object is behind camera
                return None


class Plane:
    def __init__(self, point: Point, normal: Vector, colorRGB: tuple):
        self.point = point
        self.normal = normal
        self.colorRGB = colorRGB

    def __repr__(self):
        return f"Plane({self.point}, {self.normal}, {self.colorRGB})"

    class IntersectOutput:
        def __init__(self, intersectPoint: Point, t):
            self.intersectPoint = intersectPoint
            self.t = t

    def intersect(self, origin: Point, direction: Vector):
        denom = self.normal.x * direction.x + self.normal.y * direction.y + self.normal.z * direction.z
        if denom != 0:
            diff = point_subtract(self.point, origin)
            t = (diff.x * self.normal.x + diff.y * self.normal.y + diff.z * self.normal.z) / denom
            if t >= 0:
                intersect_point = self.IntersectOutput(Point(origin.x + t * direction.x,
                                                             origin.y + t * direction.y,
                                                             origin.z + t * direction.z),
                                                             t)
                return intersect_point
        return None
    
def point_subtract(p1: Point, p2: Point) -> Vector:
    return Vector(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)


def cross(v1: Vector, v2: Vector) -> Vector:
    return Vector(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )
