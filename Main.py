from Elements import Point, Vector, Sphere, Plane
from Camera import Camera, Ray

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
    camera = Camera(Point(0, 0, 0), Point(0, 0, -5), Vector(0, 1, 0), 1.0, height, width)
    
    sphere = Sphere(Point(0, 0, -10), 3, Vector(1, 0, 0))  # Red sphere
    plane = Plane(Point(0, -3, -10), Vector(0, 1, 0), Vector(0, 1, 0))  # Green plane

    objects = []

    objects.append(sphere)
    objects.append(plane)

    image = camera.raycast(objects)

    write_ppm(image, width, height, "output.ppm")
    print("Image written to output.ppm")


if __name__ == "__main__":
    main()
