# defines elements of R3
import statistics

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other) : 
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False
    
    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]

    def get_magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def get_normalized(self):
        magnitude = self.get_magnitude()
        if magnitude == 0:
            return Vector(0, 0, 0)
        return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)

class IntersectOutput:
    def __init__(self, intersectPoint: Point, t, normal: Vector, obj):
        self.intersectPoint = intersectPoint
        self.t = t
        self.normal = normal
        self.obj = obj

class Sphere:
    def __init__(self, center: Point, radius: float, k_ambient: Vector, k_diffuse: Vector, k_specular: Vector, k_reflection: Vector, k_transmission: Vector, refractIndex, n_coef):
        self.center = center
        self.radius = radius
        self.k_ambient = k_ambient
        self.k_diffuse = k_diffuse
        self.k_specular = k_specular
        self.k_reflection = k_reflection
        self.k_transmission = k_transmission
        self.refractIndex = refractIndex
        self.n_coef = n_coef

    def __repr__(self):
        return f"Sphere({self.center}, {self.radius})"

    def get_center(self):
        return self.center

    def intersect(self, origin: Point, direction: Vector):
        oc = point_subtract(origin, self.center)
        a = direction.x**2 + direction.y**2 + direction.z**2
        b = 2.0 * dot_product(oc, direction)
        c = oc.x**2 + oc.y**2 + oc.z**2 - self.radius**2
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return None
        else:
            t = (-b - discriminant**0.5) / (2.0 * a)
            if t > 0.0001:
                intersect_point = Point(origin.x + t * direction.x, origin.y + t * direction.y, origin.z + t * direction.z)
                normal = point_subtract(intersect_point, self.center)
                return IntersectOutput(intersect_point, t, normal, self)
            else:
                t = (-b + discriminant**0.5) / (2.0 * a)
                if t > 0.0001:
                    intersect_point = Point(origin.x + t * direction.x, origin.y + t * direction.y, origin.z + t * direction.z)
                    normal = point_subtract(intersect_point, self.center)
                    return IntersectOutput(intersect_point, t, normal, self)
                else:
                    return None

class Plane:
    def __init__(self, point: Point, normal: Vector, k_ambient: Vector, k_diffuse: Vector, k_specular: Vector, k_reflection: Vector, k_transmission: Vector, refractIndex, n_coef):
        self.point = point
        self.normal = normal
        self.k_ambient = k_ambient
        self.k_diffuse = k_diffuse
        self.k_specular = k_specular
        self.k_reflection = k_reflection
        self.k_transmission = k_transmission
        self.refractIndex = refractIndex
        self.n_coef = n_coef

    def __repr__(self):
        return f"Plane({self.point}, {self.normal})"

    def get_center(self):
        # Para um plano, podemos considerar o ponto base como o "centro"
        return self.point

    def intersect(self, origin: Point, direction: Vector):
        denom = dot_product(self.normal, direction)
        if denom != 0:
            diff = point_subtract(self.point, origin)
            t = (diff.x * self.normal.x + diff.y * self.normal.y + diff.z * self.normal.z) / denom
            if t > 0.001:
                intersect_point = Point(origin.x + t * direction.x, origin.y + t * direction.y, origin.z + t * direction.z)
                return IntersectOutput(intersect_point, t, self.normal, self)
        return None

    
class TriMesh:
    def __init__(self, triangleAmt, vertexAmt, vertexList, triangleList, triangleNormals, k_ambient: Vector, k_diffuse: Vector, k_specular: Vector, k_reflection: Vector, k_transmission: Vector, refractIndex, n_coef):
        self.triangleAmt = triangleAmt
        self.vertexAmt = vertexAmt
        self.vertexList = vertexList
        self.triangleList = triangleList  # Organized by index
        self.triangleNormals = triangleNormals

        self.vertexNormals = []

        for vertI in range(vertexAmt):
            x = []
            y = []
            z = []

            for triI in range(triangleAmt):
                if vertI in self.triangleList[triI]:
                    x.append(self.triangleNormals[triI].x)
                    y.append(self.triangleNormals[triI].y)
                    z.append(self.triangleNormals[triI].z)

            vertexN = Vector(statistics.mean(x), statistics.mean(y), statistics.mean(z))
            self.vertexNormals.append(vertexN)

        self.k_ambient = k_ambient
        self.k_diffuse = k_diffuse
        self.k_specular = k_specular
        self.k_reflection = k_reflection
        self.k_transmission = k_transmission
        self.refractIndex = refractIndex
        self.n_coef = n_coef

    def get_center(self):
        x = sum(vertex.x for vertex in self.vertexList) / self.vertexAmt
        y = sum(vertex.y for vertex in self.vertexList) / self.vertexAmt
        z = sum(vertex.z for vertex in self.vertexList) / self.vertexAmt
        return Point(x, y, z)

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
            if t > 0.001:
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
                    intersect_point = Point(origin.x + t * direction.x,
                                            origin.y + t * direction.y,
                                            origin.z + t * direction.z)

                    normal = self.triangleNormals[triangleIndex]

                    # checking if intersect is in a vertex
                    for vertIndex in range(len(self.vertexList)):
                        if self.vertexList[vertIndex] == intersect_point:
                            normal = self.vertexNormals[vertIndex]

                    intersect_output = IntersectOutput(intersect_point, t, normal, self)
                    return intersect_output
                else:
                    return None
        return None
    
    def intersect(self, origin: Point, direction: Vector):
        closest_intersection = None
        min_t = float('inf')
        
        for triangleIndex in range(self.triangleAmt):
            intersection = self.intersectTriangle(origin, direction, triangleIndex)
            if intersection is not None and intersection.t < min_t:
                closest_intersection = intersection
                min_t = intersection.t

        return closest_intersection


def dot_product(v1: Vector, v2: Vector):
    return (v1.x * v2.x + v1.y * v2.y + v1.z * v2.z)

def point_subtract(p1: Point, p2: Point) -> Vector:
    return Vector(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)

def vector_add(v1: Vector, v2: Vector):
    return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def vector_sub(v1: Vector, v2: Vector):
    return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def vector_scalar(scalar, v1: Vector):
    return Vector(v1.x * scalar, v1.y * scalar, v1.z * scalar)

def cross(v1: Vector, v2: Vector) -> Vector:
    return Vector(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )