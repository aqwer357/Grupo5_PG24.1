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
        b = 2.0 * dot_product(oc, direction)
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
    def __init__(self, point: Point, normal: Vector, colorRGB: Vector):
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
        denom = dot_product(self.normal, direction)
        
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
    
class TriMesh:
    def __init__(self, triangleAmt, vertexAmt, vertexList, triangleList, triangleNormals, vertexNormals, colorRGB: Vector):
        self.triangleAmt = triangleAmt
        self.vertexAmt = vertexAmt
        self.vertexList = vertexList
        self.triangleList = triangleList # Organizadas por índice
        self.triangleNormals = triangleNormals
        self.vertexNormals = vertexNormals
        self.colorRGB = colorRGB

    class IntersectOutput:
        def __init__(self, intersectPoint: Point, t):
            self.intersectPoint = intersectPoint
            self.t = t

    def intersectTriangle(self, origin: Point, direction: Vector, triangleIndex):
        denom = dot_product(self.triangleNormals[triangleIndex], direction)
        
        if denom != 0:
            # getting points to make barycentric coords
            p1 = self.vertexList[self.triangleList[triangleIndex][0]]
            p2 = self.vertexList[self.triangleList[triangleIndex][1]]
            p3 = self.vertexList[self.triangleList[triangleIndex][2]]

            diff = point_subtract(p1, origin)
            t = dot_product(diff, self.triangleNormals[triangleIndex]) / denom
            
            # if intersects with plane, check for triangle
            if t >= 0:
                intersectPlanePoint = Point(origin.x + t * direction.x,
                                            origin.y + t * direction.y,
                                            origin.z + t * direction.z)

                v0 = point_subtract(p2, p1)
                v1 = point_subtract(p3, p1)
                v2 = point_subtract(intersectPlanePoint, p1)

                d00 = dot_product(v0, v0)
                d01 = dot_product(v0, v1)
                d11 = dot_product(v1, v1)
                d20 = dot_product(v2, v0)
                d21 = dot_product(v2, v1)

                # calculating coeficients of barycentric coords
                denom = d00 * d11 - d01 * d01

                v = (d11 * d20 - d01 * d21) / denom
                w = (d00 * d21 - d01 * d20) / denom
                u = 1.0 - v - w

                if v >= 0 and w >= 0 and u >= 0:
                    intersect_point = self.IntersectOutput(intersectPlanePoint, t)
                    return intersect_point
                else:
                    return None
        return None
    
    def intersect(self, origin: Point, direction: Vector):
        closestT = 99999999
        intersect_points = []
        for triangleIndex in range(self.triangleAmt):
            intersection = self.intersectTriangle(origin, direction, triangleIndex)

            if intersection is not None:
                intersect_points.append(intersection)

        if len(intersect_points) == 0:
            return None
        else:
            return intersect_points

def dot_product(v1: Vector, v2: Vector):
    return (v1.x * v2.x + v1.y * v2.y + v1.z * v2.z)

def point_subtract(p1: Point, p2: Point) -> Vector:
    return Vector(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)

def cross(v1: Vector, v2: Vector) -> Vector:
    return Vector(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )
