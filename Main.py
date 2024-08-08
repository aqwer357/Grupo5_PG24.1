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
    width, height = 400, 400

    p0 = Point(-3, 3, -20)
    p1 = Point(3, 3, -20)
    p2 = Point(-3, -3, -20)
    p3 = Point(3, -3, -20)
    p4 = Point(20, 2, -20)


    n1 = Vector(0, 0, 1)
    n2 = Vector(0, 0, 1)

    n3 = cross(point_subtract(p3, p2), point_subtract(p4, p2))
    n3 = n3.get_normalized()

    n4 = cross(point_subtract(p0, p3), point_subtract(p4, p3))
    n4 = n4.get_normalized()

    lightSource1 = LightSource(Point(0, 1, 0), Vector(200, 200, 200))

    lightSource2 = LightSource(Point(0, 3, 0), Vector(100, 100, 100))

    camera = Camera(Point(0, 0, 0), Point(0, 0, 1), Vector(0, 1, 0), 0.5, height, width, [lightSource1])
    
    reddishK = Vector(0.2, 0, 0.1)
    greenishK = Vector(0, 0.2, 0)
    blueishK = Vector(0.1, 0, 0.2)

    colA = Vector(0.7, 0.2, 0)
    colB = Vector(0.2, 0.5, 0)
    colC = Vector(0.2, 0.1, 0.5)

    gray = Vector(0.5, 0.5, 0.5)

    specularK = Vector(0.2, 0.4, 0.2)
    diffuseK = Vector (0.3, 0.3, 0.3)

    sphere = Sphere(Point(0, 0, 6), 2, Vector(0, 0, 0), Vector(0, 0, 0),  Vector(0.1, 0.1, 0.1), Vector(0.0, 0.0, 0.0), Vector(1, 1, 1), 1.5, 100)
    plane = Plane(Point(0, -3, -10), Vector(0, 1, 0), greenishK, colB, specularK, Vector(0, 0, 0), Vector(0, 0, 0), 1, 10)

    sphere2 = Sphere(Point(0, 3, 20), 2, blueishK, colC, specularK, Vector(0, 0, 0), Vector(0, 0, 0), 1, 100)

    mesh = TriMesh(2, 
                   4, 
                   [p0, p1, p2, p3], 
                   [(0,1,2), (3,1,2)],
                   [n1, n2],
                   gray,
                   gray,
                   gray,
                   gray,
                   gray,
                   1,
                   59)



    objects = []

    objects.append(sphere)
    objects.append(sphere2)
    #objects.append(mesh)
    objects.append(plane)

    image = camera.render(objects)

    write_ppm(image, width, height, "output.ppm")
    print("Image written to output.ppm")


if __name__ == "__main__":
    main()
