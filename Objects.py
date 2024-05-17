from Elements import Point, Vector

# defines objects to be rendered

class Sphere:
    def __init__(self, center: Point, radius, colorRGB):
        self.center = center
        self.radius = radius
        
        self.colorRGB = colorRGB

    def __repr__(self):  # __repr__ is used for debugging
        return f"Sphere({self.center}, {self.radius}, {self.colorRGB})"

    def __str__(self):  # __str__ is used for printing
       return f"Sphere({self.center}, {self.radius}, {self.colorRGB})"
    
class Plane:
    def __init__(self, point: Point, normal: Vector, colorRGB):
        self.point = point
        self.normal = normal
        
        self.colorRGB = colorRGB

    def __repr__(self):  # __repr__ is used for debugging
        return f"Plane({self.point}, {self.normal}, {self.colorRGB})"

    def __str__(self):  # __str__ is used for printing
       return f"Plane({self.point}, {self.normal}, {self.colorRGB})"
    
