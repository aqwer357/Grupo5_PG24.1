# Camera.py
from Elements import Point, Vector, IntersectOutput, point_subtract, cross, vector_add, vector_sub, vector_scalar, dot_product
from Phong import phong_model
from BSP import build_bsp, intersect_ray_bsp
import math

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

        self.recursionMax = 3
        self.screenCenterVector = vector_scalar(self.dist, self.w)

        self.intersection_points = []  # Lista para armazenar pontos de interseção

    def __repr__(self):
        return f"Camera({self.pos}, {self.target}, {self.dist}, {self.hScreen}, {self.wScreen})"
    
    def render(self, objects):
        bsp_tree = build_bsp(objects)
        image = [[(0, 0, 0) for _ in range(self.wScreen)] for _ in range(self.hScreen)]

        displaceVert = vector_scalar(-(2 * 0.5 / (self.hScreen - 1)), self.v)
        displaceHort = vector_scalar(-(2 * 0.5 / (self.wScreen - 1)), self.u)
        pixel00 = vector_sub(self.screenCenterVector, vector_add(vector_scalar(0.5, self.v), vector_scalar(0.5, self.u)))

        for i in range(self.hScreen):
            for j in range(self.wScreen):
                ray = Ray(self.pos, vector_add(vector_add(vector_scalar(i, displaceVert), vector_scalar(j, displaceHort)), pixel00))

                color = self.raytrace(ray, bsp_tree, 0, 1)
                image[i][j] = (color.x, color.y, color.z)

        self.draw_intersections(image)  # Desenha pontos de interseção
        return image
    
    def raytrace(self, ray: Ray, bsp_tree, recursionAmt, inIOR):
        color = Vector(0,0,0)

        if recursionAmt >= self.recursionMax:
            return color
        
        intersection, closestT = intersect_ray_bsp(ray, bsp_tree)
        
        if intersection:
            self.intersection_points.append(intersection.intersectPoint)  # Adiciona ponto de interseção
            obj = intersection.obj
            ir = Vector(0,0,0)
            it = Vector(0,0,0)

            for source in self.lightSources:
                light = point_subtract(source.point, intersection.intersectPoint).get_normalized()
                normal = intersection.normal
                scalar = (2 * dot_product(normal, light))

                if obj.k_reflection.get_magnitude() > 0:
                    reflect = Vector((scalar*normal.x - light.x), (scalar*normal.y - light.y), (scalar*normal.z - light.z)).get_normalized()
                    reflectRay = Ray(intersection.intersectPoint, reflect)
                    reflectColor = self.raytrace(reflectRay, bsp_tree, recursionAmt+1, inIOR)
                    ir = Vector(reflectColor.x + ir.x, reflectColor.y + ir.y, reflectColor.z + ir.z)

                if obj.k_transmission.get_magnitude() > 0.0001:
                    n = intersection.normal.get_normalized()
                    i = ray.direction.get_normalized()
                    cosIN = dot_product(i, n)
                    if cosIN < 0.001:
                        cosIN = -1*cosIN
                        n = vector_scalar(-1, n)
                    senIN = math.sqrt(1 - (cosIN * cosIN))
                    ior = obj.refractIndex/inIOR
                    senOUT = senIN/ior
                    cosOUT = math.sqrt(1 - (senOUT * senOUT))
                    refract = vector_sub(vector_scalar(1/ior, i), vector_scalar(cosOUT - (1/ior*cosIN), n))
                    transRay = Ray(intersection.intersectPoint, refract)
                    it = self.raytrace(transRay, bsp_tree, recursionAmt+1, obj.refractIndex)

            color = phong_model(ray.origin, intersection.intersectPoint, self.lightSources, intersection.normal,
                                obj.k_ambient, obj.k_diffuse, obj.k_specular, obj.k_reflection, obj.k_transmission, obj.n_coef, ir, it)
        
        return color

    def draw_intersections(self, image):
        for point in self.intersection_points:
            x = int(point.x)
            y = int(point.y)
            if 0 <= x < self.wScreen and 0 <= y < self.hScreen:
                image[y][x] = (255, 0, 0)  # Desenha o ponto de interseção em vermelho
