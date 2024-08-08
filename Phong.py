from Elements import Point, Vector, point_subtract, dot_product, vector_scalar, is_shadowed

class LightSource:
    def __init__(self, center: Point, lightColor: Vector):
        self.center = center
        self.lightColor = lightColor

    def intensityAt(self, point, objects):
        return 1 - is_shadowed(point, self.center, objects)


def phong_model(objects, viewPos: Point, intersectPoint: Point, lightSources, normal: Vector, ka: Vector, kd: Vector, ks: Vector, kr: Vector, kt: Vector, n, ir=Vector(0,0,0), it=Vector(0,0,0)):
    
    view = point_subtract(viewPos, intersectPoint).get_normalized()

    # Ambient light coefficient
    ia = Vector(60, 60, 60)

    normal = normal.get_normalized()
    

    # Actual color calculation

    colorResult = Vector(ka.x * ia.x, ka.y * ia.y, ka.z * ia.z)
    for source in lightSources:
        lightIntensity = source.intensityAt(intersectPoint, objects)

        light = point_subtract(source.center,intersectPoint).get_normalized()
        scalar = (2 * dot_product(normal, light))
        reflect = Vector((scalar*normal.x - light.x), (scalar*normal.y - light.y), (scalar*normal.z - light.z)).get_normalized()
        il = source.lightColor
        il = vector_scalar(lightIntensity, source.lightColor)

        r = (il.x * (kd.x * (dot_product(normal,light)) + ks.x * (dot_product(reflect,view))**n)) + kr.x * ir.x + kt.x * it.x
        g = (il.y * (kd.y * (dot_product(normal,light)) + ks.y * (dot_product(reflect,view))**n)) + kr.y * ir.y + kt.y * it.y
        b = (il.y * (kd.z * (dot_product(normal,light)) + ks.z * (dot_product(reflect,view))**n)) + kr.z * ir.z + kt.z * it.z

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