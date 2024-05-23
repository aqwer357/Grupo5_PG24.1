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
    plane = Plane(Point(0, -3, -10), Vector(0, 1, 0), (0, 1, 0))  # Green plane

    image = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

    intersects_sphere = False
    intersects_plane = False

    for i in range(height):
        for j in range(width):
            x = (2 * (j + 0.5) / width - 1) * (width / height)
            y = 1 - 2 * (i + 0.5) / height
            ray = Ray(camera.pos, Vector(x, y, -1))

            sphere_intersection = sphere.intersect(ray.origin, ray.direction)
            if sphere_intersection:
                image[i][j] = (100, 0, 0) #vermelho
                intersects_sphere = True
            else:
                plane_intersection = plane.intersect(ray.origin, ray.direction)
                if plane_intersection:
                    image[i][j] = (0, 255, 0) #verde
                    intersects_plane = True

    if intersects_plane and intersects_sphere:
        print("O raio intercepta o plano e a esfera.")
    elif intersects_plane:
        print("O raio intercepta o plano.")
    elif intersects_sphere:
        print("O raio intercepta a esfera.")
    else:
        print("O raio não intercepta nem a esfera nem o plano.")

    write_ppm(image, width, height, "output.ppm")
    print("Image written to output.ppm")


if __name__ == "__main__":
    main()
