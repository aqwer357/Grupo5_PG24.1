from Elements import Point, Vector, IntersectOutput, point_subtract, cross, vector_add, vector_sub, vector_scalar, dot_product
from Phong import phong_model
import math

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

        self.recursionMax = 4
        self.screenCenterVector = vector_scalar(self.dist, self.w)

    def __repr__(self):
        return f"Camera({self.pos}, {self.target}, {self.dist}, {self.hScreen}, {self.wScreen})"
    
    def render(self, objects):
        image = [[(0, 0, 0) for _ in range(self.wScreen)] for _ in range(self.hScreen)]

        displaceVert = vector_scalar(-(2 * 0.5 / (self.hScreen - 1)), self.v)
        displaceHort = vector_scalar(-(2 * 0.5 / (self.wScreen - 1)), self.u)
        pixel00 = vector_sub(self.screenCenterVector, vector_add(vector_scalar(0.5, self.v), vector_scalar(0.5, self.u)))

        for i in range(self.hScreen):
            for j in range(self.wScreen):
                
                ray = Ray(self.pos, vector_add(vector_add(vector_scalar(i, displaceVert), vector_scalar(j, displaceHort)), pixel00))

                color = self.raytrace(ray, objects, 0)
                image[i][j] = (color.x, color.y, color.z)

        return image
    
    def raytrace(self, ray: Ray, objects, recursionAmt):
        color = Vector(0,0,0)
        closestT = 99999999
        if recursionAmt >= self.recursionMax:
            return color
        for obj in objects:
            intersection = obj.intersect(ray.origin, ray.direction)

            if intersection is not None:
                if obj.__class__.__name__ == 'TriMesh':
                    for intersect in intersection:
                        # TriMesh returns intersection list and this for parses them
                        if intersect.t < closestT:
                            closestT = intersect.t
                            
                            for source in self.lightSources:
                                light = point_subtract(source.point, intersect.intersectPoint).get_normalized()
                                normal = intersect.normal
                                scalar = (2 * dot_product(normal, light))

                                ir = Vector(0,0,0)
                                for source in self.lightSources:
                                    light = point_subtract(source.point, intersection.intersectPoint).get_normalized()
                                    normal = intersection.normal
                                    scalar = (2 * dot_product(normal, light))

                                    if obj.k_reflection.get_magnitude() > 0:
                                        reflect = Vector((scalar*normal.x - light.x), (scalar*normal.y - light.y), (scalar*normal.z - light.z)).get_normalized()
                                        reflectRay = Ray(intersection.intersectPoint, reflect)

                                        reflectColor = self.raytrace(reflectRay, objects, recursionAmt+1)
                                        
                                        ir = Vector(reflectColor.x + ir.x, reflectColor.y + ir.y, reflectColor.z + ir.z)
                                
                                color = phong_model(ray.origin, intersection.intersectPoint, self.lightSources, intersection.normal,
                                                    obj.k_ambient, obj.k_diffuse, obj.k_specular, obj.k_reflection, obj.k_transmission, obj.n_coef, ir)
                                ## REFRACTION - WIP ##
                                # if obj.k_transmission.get_magnitude() > 0:
                                #     n = intersect.normal
                                #     cos = dot_product(ray.direction, intersect.normal)
                                #     ior = obj.refractIndex

                                #     if cos < 0:
                                #         n = vector_scalar(-1, n)
                                #         ior = 1 / ior
                                #         cos = -1 * cos

                                #     delta = 1 - (1 - cos * cos) / (ior * ior)

                                #     if delta >=0:
                                #         refract =             
                elif intersection.t < closestT:
                    closestT = intersection.t
                    
                    ir = Vector(0,0,0)
                    for source in self.lightSources:
                        light = point_subtract(source.point, intersection.intersectPoint).get_normalized()
                        normal = intersection.normal
                        scalar = (2 * dot_product(normal, light))

                        if obj.k_reflection.get_magnitude() > 0:
                            reflect = Vector((scalar*normal.x - light.x), (scalar*normal.y - light.y), (scalar*normal.z - light.z)).get_normalized()
                            reflectRay = Ray(intersection.intersectPoint, reflect)

                            reflectColor = self.raytrace(reflectRay, objects, recursionAmt+1)
                            
                            ir = Vector(reflectColor.x + ir.x, reflectColor.y + ir.y, reflectColor.z + ir.z)
                    
                    color = phong_model(ray.origin, intersection.intersectPoint, self.lightSources, intersection.normal,
                                        obj.k_ambient, obj.k_diffuse, obj.k_specular, obj.k_reflection, obj.k_transmission, obj.n_coef, ir)
            
        return color