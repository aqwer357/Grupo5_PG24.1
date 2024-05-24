from Elements import Point, Vector, Sphere, Plane, TriMesh, cross, point_subtract
from Camera import Camera

def write_ppm(image, width, height, filename):
    with open(filename, 'w') as f:
        f.write("P3\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")
        for row in image:
            for color in row:
                r, g, b = color
                f.write(f"{r} {g} {b} ")
            f.write("\n")


def main():
    width, height = 800, 600

    p0 = Point(10, 6, -8)
    p1 = Point(0, 5, -8)
    p2 = Point(-10, 2, -8)
    p3 = Point(0, -1, -6)
    p4 = Point(20, 2, -10)

    n1 = cross(point_subtract(p1, p0), point_subtract(p4, p0))
    n1 = n1.get_normalized()

    n2 = cross(point_subtract(p2, p1), point_subtract(p4, p1))
    n2 = n2.get_normalized()

    n3 = cross(point_subtract(p3, p2), point_subtract(p4, p2))
    n3 = n3.get_normalized()

    n4 = cross(point_subtract(p0, p3), point_subtract(p4, p3))
    n4 = n4.get_normalized()

    camera = Camera(Point(0, 0, 0), Point(0, 0, -5), Vector(0, 1, 0), 1.0, height, width)
    
    sphere = Sphere(Point(0, 0, -10), 3, Vector(1, 0, 0))  # Red sphere
    plane = Plane(Point(0, -2, -10), Vector(0, 1, 0), Vector(0, 1, 0))  # Green plane

    mesh = TriMesh(4, 
                   5, 
                   [p0, p1, p2, p3, p4], 
                   [(0,1,4),(1,2,4),(2,3,4),(0,3,4)],
                   [n1,n2,n3,n4],
                   [],
                   Vector(0,0,1)) # Blue mesh

    objects = []

    objects.append(sphere)
    objects.append(plane)
    objects.append(mesh)

    image = camera.raycast(objects)

    write_ppm(image, width, height, "output.ppm")
    print("Image written to output.ppm")


if __name__ == "__main__":
    main()
