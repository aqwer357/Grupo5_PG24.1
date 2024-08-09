from Elements import Point, Vector, Sphere, Plane, TriMesh

class BSPNode:
    def __init__(self, objects, axis=None, median_value=None, left=None, right=None):
        self.objects = objects
        self.axis = axis
        self.median_value = median_value
        self.left = left
        self.right = right

def get_axis_value(point, axis):
    if axis == 0:
        return point.x
    elif axis == 1:
        return point.y
    elif axis == 2:
        return point.z
    return 0  # Caso padrão, embora não deva ser necessário

def intersect_ray_bsp(ray, node):
    if node.objects is not None:
        closest_t = float('inf')
        closest_intersection = None
        for obj in node.objects:
            result = obj.intersect(ray.origin, ray.direction)
            if result is not None:
                intersection, t = result.intersectPoint, result.t
                if t < closest_t:
                    closest_t = t
                    closest_intersection = result
        if closest_intersection is not None:
            return closest_intersection, closest_t
        return None, None
    
    # Caso contrário, recursivamente verificar os nós filhos
    first_node, second_node = (node.left, node.right) if ray.direction[node.axis] >= 0 else (node.right, node.left)
    
    # Tentar o primeiro nó
    obj, t = intersect_ray_bsp(ray, first_node)
    if obj is not None:
        return obj, t
    
    # Tentar o segundo nó se o primeiro falhar
    return intersect_ray_bsp(ray, second_node)

def choose_axis(objects):
    # Calcula a variação em cada eixo (x, y, z) e retorna o eixo com a maior variação
    x_variance = max(obj.get_center().x for obj in objects) - min(obj.get_center().x for obj in objects)
    y_variance = max(obj.get_center().y for obj in objects) - min(obj.get_center().y for obj in objects)
    z_variance = max(obj.get_center().z for obj in objects) - min(obj.get_center().z for obj in objects)
    
    variances = [x_variance, y_variance, z_variance]
    return variances.index(max(variances))

def build_bsp(objects, depth=0, max_depth=10):
    if len(objects) <= 1 or depth >= max_depth:
        return BSPNode(objects=objects, axis=None, median_value=None)
    
    axis = choose_axis(objects)
    
    objects.sort(key=lambda obj: obj.get_center()[axis])
    median_index = len(objects) // 2
    median_value = getattr(objects[median_index].get_center(), ['x', 'y', 'z'][axis])
    
    left_objects = objects[:median_index]
    right_objects = objects[median_index:]
    
    # Aqui, se um objeto está exatamente no plano de corte, ele vai para o lado direito para evitar divisão infinita.
    if not left_objects or not right_objects:
        left_objects = objects[:median_index]  # Reajustar caso um dos lados tenha ficado vazio
        right_objects = objects[median_index:]
    
    left = build_bsp(left_objects, depth + 1, max_depth)
    right = build_bsp(right_objects, depth + 1, max_depth)
    
    return BSPNode(left=left, right=right, axis=axis, median_value=median_value, objects=None)
