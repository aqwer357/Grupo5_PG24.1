from Elements import Point, Vector, Sphere, Plane
from Camera import Camera
from Phong import LightSource

def write_ppm(image, width, height, filename):
    with open(filename, 'w') as f:
        f.write("P3\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")
        for row in image:
            for color in row:
                r, g, b = color
                f.write(f"{int(r)} {int(g)} {int(b)} ")
            f.write("\n")

def render_scene(spheres, planes, lights, camera_pos, output_filename):
    width, height = 400, 400
    objects = spheres + planes
    camera = Camera(camera_pos, Point(0, 0, 1), Vector(0, 1, 0), 0.5, height, width, lights)
    image = camera.render(objects)
    write_ppm(image, width, height, output_filename)
    print(f"Imagem salva em {output_filename}")

def main():
    scenarios = [
        # Cenário 1: Distribuição Horizontal
        {
            "spheres": [
                Sphere(Point(-4, 0, 10), 1.5, Vector(0.1, 0.1, 0.1), Vector(0.7, 0.2, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100),
                Sphere(Point(0, 0, 10), 1.5, Vector(0.1, 0.1, 0.1), Vector(0.2, 0.7, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100),
                Sphere(Point(4, 0, 10), 1.5, Vector(0.1, 0.1, 0.1), Vector(0.2, 0.2, 0.7), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100)
            ],
            "planes": [
                Plane(Point(0, -3, -10), Vector(0, 1, 0), Vector(0.2, 0.2, 0.2), Vector(0.7, 0.7, 0.7), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1, 10)
            ],
            "lights": [LightSource(Point(0, 10, -10), Vector(200, 200, 200))],
            "camera_pos": Point(0, 0, -20),
            "output_filename": "output1.ppm"
        },
        # Cenário 2: Distribuição Vertical
        {
            "spheres": [
                Sphere(Point(0, -4, 10), 1.5, Vector(0.1, 0.1, 0.1), Vector(0.7, 0.7, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100),
                Sphere(Point(0, 0, 10), 1.5, Vector(0.1, 0.1, 0.1), Vector(0.7, 0.2, 0.7), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100),
                Sphere(Point(0, 4, 10), 1.5, Vector(0.1, 0.1, 0.1), Vector(0.2, 0.7, 0.7), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100)
            ],
            "planes": [
                Plane(Point(0, -3, -10), Vector(0, 1, 0), Vector(0.2, 0.2, 0.2), Vector(0.7, 0.7, 0.7), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1, 10)
            ],
            "lights": [LightSource(Point(0, 10, -10), Vector(200, 200, 200))],
            "camera_pos": Point(0, 0, -20),
            "output_filename": "output2.ppm"
        },
        # Cenário 3: Distribuição em Profundidade
        {
            "spheres": [
                Sphere(Point(0, 0, 8), 1.5, Vector(0.1, 0.1, 0.1), Vector(0.2, 0.7, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100),
                Sphere(Point(0, 0, 10), 1.5, Vector(0.1, 0.1, 0.1), Vector(0.2, 0.2, 0.7), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100),
                Sphere(Point(0, 0, 12), 1.5, Vector(0.1, 0.1, 0.1), Vector(0.7, 0.2, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100)
            ],
            "planes": [
                Plane(Point(0, -3, -10), Vector(0, 1, 0), Vector(0.2, 0.2, 0.2), Vector(0.7, 0.7, 0.7), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1, 10)
            ],
            "lights": [LightSource(Point(0, 10, -10), Vector(200, 200, 200))],
            "camera_pos": Point(0, 0, -20),
            "output_filename": "output3.ppm"
        }
    ]

    for scenario in scenarios:
        render_scene(
            scenario["spheres"],
            scenario["planes"],
            scenario["lights"],
            scenario["camera_pos"],
            scenario["output_filename"]
        )

if __name__ == "__main__":
    main()
