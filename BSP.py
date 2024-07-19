class BSPNode:
    def __init__(self, objects, axis, left, right):
        self.objects = objects
        self.axis = axis
        self.left = left
        self.right = right

def get_axis_value(point, axis):
    if axis == 0:
        return point.x
    elif axis == 1:
        return point.y
    elif axis == 2:
        return point.z
    return 0

def build_bsp(objects, depth=0):
    if not objects:
        return None

    axis = depth % 3  # Alterna entre x, y, z

    objects.sort(key=lambda obj: get_axis_value(obj.center if hasattr(obj, 'center') else obj.point, axis))
    median = len(objects) // 2

    left = build_bsp(objects[:median], depth + 1)
    right = build_bsp(objects[median + 1:], depth + 1)

    return BSPNode(objects, axis, left, right)

def intersect_ray_bsp(ray, node):
    if not node:
        return None, float('inf')

    hit_obj = None
    min_t = float('inf')

    for obj in node.objects:
        intersection = obj.intersect(ray.origin, ray.direction)
        if intersection and intersection.t < min_t:
            hit_obj = intersection
            min_t = intersection.t

    axis = node.axis
    origin_axis_value = get_axis_value(ray.origin, axis)
    left_first = origin_axis_value < get_axis_value(node.objects[0].center if hasattr(node.objects[0], 'center') else node.objects[0].point, axis)

    first = node.left if left_first else node.right
    second = node.right if left_first else node.left

    hit_first, t_first = intersect_ray_bsp(ray, first)
    if hit_first and t_first < min_t:
        hit_obj = hit_first
        min_t = t_first

    hit_second, t_second = intersect_ray_bsp(ray, second)
    if hit_second and t_second < min_t:
        hit_obj = hit_second
        min_t = t_second

    return hit_obj, min_t
