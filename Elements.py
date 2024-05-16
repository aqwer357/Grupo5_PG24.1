# defines the essential elements of the cartesian plane

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):  # __repr__ is used for debugging
        return f"Point({self.x}, {self.y}, {self.z})"

    def __str__(self):  # __str__ is used for printing
        return f"({self.x}, {self.y}, {self.z})"
    
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):  # __repr__ is used for debugging
        return f"Point({self.x}, {self.y}, {self.z})"

    def __str__(self):  # __str__ is used for printing
        return f"({self.x}, {self.y}, {self.z})"
    
    def getMagnitude(self):
        magnitude = (self.x**2 + self.y**2 + self.z**2)**0.5
        return magnitude

    def getNormalized(self):
        normSelf = Vector(self.x/self.getMagnitude(),self.y/self.getMagnitude(),self.z/self.getMagnitude())
        return normSelf
