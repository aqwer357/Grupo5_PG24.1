from Elements import Point, Vector, point_subtract, dot_product

class LightSource:
    def __init__(self, point: Point, lightColor: Vector):
        self.point = point
        self.lightColor = lightColor


def phong_model(viewPos: Point, intersectPoint: Point, lightSources, normal: Vector, ka: Vector, kd: Vector, ks: Vector, kr: Vector, kt: Vector, n):
    
    view = point_subtract(viewPos, intersectPoint).get_normalized()

    # Ambient light coefficient
    ia = Vector(60, 60, 0)

    normal = normal.get_normalized()
    

    # Actual color calculation

    colorResult = Vector(ka.x * ia.x, ka.y * ia.y, ka.z * ia.z)
    for source in lightSources:
        light = point_subtract(source.point,intersectPoint).get_normalized()
        scalar = (2 * dot_product(normal, light))
        reflect = Vector((scalar*normal.x - light.x), (scalar*normal.y - light.y), (scalar*normal.y - light.y)).get_normalized()
        il = source.lightColor

        r = (il.x * (kd.x * (dot_product(normal,light)) + ks.x * (dot_product(reflect,view))**n))
        g = (il.y * (kd.y * (dot_product(normal,light)) + ks.y * (dot_product(reflect,view))**n))
        b = (il.y * (kd.y * (dot_product(normal,light)) + ks.y * (dot_product(reflect,view))**n))

        colorResult.x += r
        colorResult.y += g
        colorResult.z += b

    # clamping values to 255
    if colorResult.x > 255:
        colorResult.x = 255
    if colorResult.y > 255:
        colorResult.y = 255
    if colorResult.z > 255:
        colorResult.z = 255

    # for raytracing, result += kr * ir + kt * it
    return colorResult