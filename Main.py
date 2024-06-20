from Elements import Point, Vector, Sphere, Plane, TriMesh, cross, point_subtract
from Camera import Camera
from Transforms import affine_transform
from Phong import LightSource

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

    p0 = Point(-3, 3, -10)
    p1 = Point(3, 3, -10)
    p2 = Point(-3, -3, -10)
    p3 = Point(3, -3, -10)
    p4 = Point(20, 2, -10)

    p0 = affine_transform(p0, "rotate_x", 0, 0, 2, 45)
    p1 = affine_transform(p1, "rotate_x", 0, 0, 2, 45)
    p2 = affine_transform(p2, "rotate_x", 0, 0, 2, 45)
    p3 = affine_transform(p3, "rotate_x", 0, 0, 2, 45)

    n1 = cross(point_subtract(p1, p0), point_subtract(p2, p0))
    n1 = n1.get_normalized()

    n2 = cross(point_subtract(p2, p1), point_subtract(p3, p1))
    n2 = n2.get_normalized()

    n3 = cross(point_subtract(p3, p2), point_subtract(p4, p2))
    n3 = n3.get_normalized()

    n4 = cross(point_subtract(p0, p3), point_subtract(p4, p3))
    n4 = n4.get_normalized()

    lightSource1 = LightSource(Point(0, 10, -20), Vector(200, 200, 200))

    camera = Camera(Point(0, 0, 0), Point(0, 0, -5), Vector(0, 1, 0), 1.0, height, width, [lightSource1])
    
    reddishK = Vector(0.2, 0, 0)
    greenishK = Vector(0, 0.2, 0)

    colA = Vector(0.7, 0.2, 0)
    colB = Vector(0.2, 0.5, 0)

    specularK = Vector(0.4, 0.4, 0.4)
    diffuseK = Vector (0.3, 0.3, 0.3)

    sphere = Sphere(Point(0, 0, -10), 3, reddishK, colA, specularK, reddishK, reddishK, 100)
    plane = Plane(Point(0, -2, -10), Vector(0, 1, 0), greenishK, colB, specularK, greenishK, greenishK, 10)

    # mesh = TriMesh(2, 
    #                4, 
    #                [p0, p1, p2, p3], 
    #                [(0,1,2), (3,1,2)],
    #                [n1, n2],
    #                [],
    #                Vector(0,0,1)) # Blue mesh

    objects = []

    objects.append(sphere)
    objects.append(plane)
    #objects.append(mesh)

    image = camera.raycast(objects)

    write_ppm(image, width, height, "output.ppm")
    print("Image written to output.ppm")


if __name__ == "__main__":
    main()
