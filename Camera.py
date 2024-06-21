from Elements import Point, Vector, IntersectOutput, point_subtract, cross, vector_add, vector_sub, vector_scalar
from Phong import phong_model

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
    def __init__(self, pos: Point, target: Point, up: Vector, dist: float, hScreen: int, wScreen: int, lightSources):
        self.pos = pos
        self.target = target
        self.w = point_subtract(target, pos).get_normalized()
        self.u = cross(up, self.w).get_normalized()
        self.v = up.get_normalized()
        self.dist = dist
        self.hScreen = hScreen
        self.wScreen = wScreen
        self.lightSources = lightSources

        self.screenCenterVector = vector_scalar(self.dist, self.w)

    def __repr__(self):
        return f"Camera({self.pos}, {self.target}, {self.dist}, {self.hScreen}, {self.wScreen})"
    
    def raycast(self, objects):
        image = [[(0, 0, 0) for _ in range(self.wScreen)] for _ in range(self.hScreen)]

        displaceVert = vector_scalar(-(2 * 0.5 / (self.hScreen - 1)), self.v)
        displaceHort = vector_scalar(-(2 * 0.5 / (self.wScreen - 1)), self.u)
        pixel00 = vector_sub(self.screenCenterVector, vector_add(vector_scalar(0.5, self.v), vector_scalar(0.5, self.u)))

        for i in range(self.hScreen):
            for j in range(self.wScreen):
                
                ray = Ray(self.pos, vector_add(vector_add(vector_scalar(i, displaceVert), vector_scalar(j, displaceHort)), pixel00))

                # allows us to know which object is closest by using scalar of ray
                closestT = 99999999
                
                for obj in objects:
                    intersection = obj.intersect(ray.origin, ray.direction)

                    if intersection is not None:
                        if obj.__class__.__name__ == 'TriMesh':
                                for intersect in intersection:
                                    # TriMesh returns intersection list and this for parses them
                                    if intersect.t < closestT:
                                        closestT = intersect.t
                                        color = phong_model(self.pos, intersect.intersectPoint, self.lightSources, intersect.normal,
                                                             obj.k_ambient, obj.k_diffuse, obj.k_specular, obj.k_reflection, obj.k_transmission, obj.n_coef)

                                        image[i][j] = (color.x, color.y, color.z)
                        elif intersection.t < closestT:
                            closestT = intersection.t
                            color = phong_model(self.pos, intersection.intersectPoint, self.lightSources, intersection.normal,
                                                obj.k_ambient, obj.k_diffuse, obj.k_specular, obj.k_reflection, obj.k_transmission, obj.n_coef)
                            
                            image[i][j] = (color.x, color.y, color.z)

        return image