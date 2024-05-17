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


class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction.get_normalized()

    def __repr__(self):
        return f"Ray({self.origin}, {self.direction})"

    def __str__(self):
        return f"Ray({self.origin}, {self.direction})"


def point_subtract(p1: Point, p2: Point) -> Vector:
    return Vector(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)


def cross(v1: Vector, v2: Vector) -> Vector:
    return Vector(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )


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


class Sphere:
    def __init__(self, center: Point, radius: float, colorRGB: Vector):
        self.center = center
        self.radius = radius
        self.colorRGB = colorRGB

    def __repr__(self):
        return f"Sphere({self.center}, {self.radius}, {self.colorRGB})"

    def intersect(self, ray: Ray):
        oc = point_subtract(ray.origin, self.center)
        a = ray.direction.x**2 + ray.direction.y**2 + ray.direction.z**2
        b = 2.0 * (oc.x * ray.direction.x + oc.y * ray.direction.y + oc.z * ray.direction.z)
        c = oc.x**2 + oc.y**2 + oc.z**2 - self.radius**2
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return None
        else:
            t = (-b - discriminant**0.5) / (2.0 * a)
            if t >= 0:
                intersect_point = Point(ray.origin.x + t * ray.direction.x,
                                        ray.origin.y + t * ray.direction.y,
                                        ray.origin.z + t * ray.direction.z)
                return intersect_point
            else:
                return None


class Plane:
    def __init__(self, point: Point, normal: Vector, colorRGB: tuple):
        self.point = point
        self.normal = normal
        self.colorRGB = colorRGB

    def __repr__(self):
        return f"Plane({self.point}, {self.normal}, {self.colorRGB})"

    def intersect(self, ray: Ray):
        denom = self.normal.x * ray.direction.x + self.normal.y * ray.direction.y + self.normal.z * ray.direction.z
        if denom != 0:
            diff = point_subtract(self.point, ray.origin)
            t = (diff.x * self.normal.x + diff.y * self.normal.y + diff.z * self.normal.z) / denom
            if t >= 0:
                intersect_point = Point(ray.origin.x + t * ray.direction.x,
                                        ray.origin.y + t * ray.direction.y,
                                        ray.origin.z + t * ray.direction.z)
                return intersect_point
        return None


def write_ppm(image, width, height, filename):
    with open(filename, 'w') as f:
        f.write("P3\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")
        for row in image:
            for color in row:
                r, g, b = color
                f.write(f"{r} {g} {b} ")
            f.write("\n")


def main():
    width, height = 800, 600
    camera = Camera(Point(0, 0, 0), Point(0, 0, -5), Vector(0, 1, 0), 1.0, height, width)
    
    sphere = Sphere(Point(0, 0, -10), 3, Vector(1, 0, 0))  # Red sphere
    plane = Plane(Point(0, -3, -10), Vector(0, 1, 0), (0, 1, 0))  # Green plane

    image = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

    intersects_sphere = False
    intersects_plane = False

    for i in range(height):
        for j in range(width):
            x = (2 * (j + 0.5) / width - 1) * (width / height)
            y = 1 - 2 * (i + 0.5) / height
            ray = Ray(camera.pos, Vector(x, y, -1))

            sphere_intersection = sphere.intersect(ray)
            if sphere_intersection:
                image[i][j] = (100, 0, 0) #vermelho
                intersects_sphere = True
            else:
                plane_intersection = plane.intersect(ray)
                if plane_intersection:
                    image[i][j] = (0, 255, 0) #verde
                    intersects_plane = True

    if intersects_plane and intersects_sphere:
        print("O raio intercepta o plano e a esfera.")
    elif intersects_plane:
        print("O raio intercepta o plano.")
    elif intersects_sphere:
        print("O raio intercepta a esfera.")
    else:
        print("O raio não intercepta nem a esfera nem o plano.")

    write_ppm(image, width, height, "output.ppm")
    print("Image written to output.ppm")


if __name__ == "__main__":
    main()
