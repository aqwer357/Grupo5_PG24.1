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
    
    def raycast(self, objects):
        image = [[(0, 0, 0) for _ in range(self.wScreen)] for _ in range(self.hScreen)]

        for i in range(self.hScreen):
            for j in range(self.wScreen):
                x = (2 * (j + 0.5) / self.wScreen - 1) * (self.wScreen / self.hScreen)
                y = 1 - 2 * (i + 0.5) / self.hScreen
                ray = Ray(self.pos, Vector(x, y, -1))

                # allows us to know which object is closest by using scalar of ray
                closestT = 99999999
                
                for obj in objects:
                    intersection = obj.intersect(ray.origin, ray.direction)

                    if intersection is not None and intersection.t < closestT:
                        closestT = intersection.t
                        color = obj.colorRGB
                        # *255 is used to convert values to regular RGB notation
                        image[i][j] = (color.x * 255, color.y * 255, color.z * 255)

        return image