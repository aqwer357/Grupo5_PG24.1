from Elements import Point, Vector, Sphere, Plane, TriMesh
from Camera import Camera
from Phong import LightSource

# Function to save the rendered image as a PPM file
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

# Function to render the scene
def render_scene(spheres, planes, meshes, lights, camera_pos, output_filename, resolution=(800, 800)):
    width, height = resolution
    objects = spheres + planes + meshes
    camera = Camera(camera_pos, Point(0, 0, 1), Vector(0, 1, 0), 0.5, height, width, lights)
    
    # The `render` function from the `Camera` class is called with the list of objects
    image = camera.render(objects)
    
    write_ppm(image, width, height, output_filename)
    print(f"Image saved as {output_filename}, with resolution {width}x{height}")

# Cenário específico para renderizar os triângulos que mostram a funcionalidade BSP
def render_intersecting_triangles_large():
    triangle1 = TriMesh(
        triangleAmt=1,
        vertexAmt=3,
        vertexList=[Point(-1, -1, 5), Point(4, -1, 5), Point(1.5, 4, 5)],
        triangleList=[[0, 1, 2]],
        triangleNormals=[Vector(0, 0, -1)],
        k_ambient=Vector(0.1, 0.1, 0.1),
        k_diffuse=Vector(0.7, 0.2, 0.2),
        k_specular=Vector(1, 1, 1),
        k_reflection=Vector(0.3, 0.3, 0.3),
        k_transmission=Vector(0, 0, 0),
        refractIndex=1.5,
        n_coef=100
    )

    triangle2 = TriMesh(
        triangleAmt=1,
        vertexAmt=3,
        vertexList=[Point(0, -3, 6), Point(5, -3, 6), Point(2.5, 2, 6)],
        triangleList=[[0, 1, 2]],
        triangleNormals=[Vector(0, 0, -1)],
        k_ambient=Vector(0.1, 0.1, 0.1),
        k_diffuse=Vector(0.2, 0.7, 0.2),
        k_specular=Vector(1, 1, 1),
        k_reflection=Vector(0.3, 0.3, 0.3),
        k_transmission=Vector(0, 0, 0),
        refractIndex=1.5,
        n_coef=100
    )

    light = LightSource(Point(0, 10, -10), Vector(200, 200, 200))
    camera_pos = Point(0, 0, -10)

    render_scene(
        spheres=[],  # No spheres
        planes=[],  # No planes
        meshes=[triangle1, triangle2],  # Just the triangles
        lights=[light],
        camera_pos=camera_pos,
        output_filename="intersecting_triangles_large.ppm",
        resolution=(800, 800)
    )

# Main function to set up and render the scenes
def main():
    scenarios = [
        # Cenário 1: Teste de Divisão BSP com Esferas e Planos
        {
            "spheres": [
                Sphere(Point(-2, 0, 10), 2, Vector(0.1, 0.1, 0.1), Vector(0.7, 0.2, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100),
                Sphere(Point(2, 0, 15), 3, Vector(0.1, 0.1, 0.1), Vector(0.2, 0.7, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100)
            ],
            "planes": [
                Plane(Point(0, -3, 10), Vector(0, 1, 0), Vector(0.2, 0.2, 0.2), Vector(0.7, 0.7, 0.7), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1, 10)
            ],
            "meshes": [],
            "lights": [LightSource(Point(0, 10, -10), Vector(200, 200, 200))],
            "camera_pos": Point(0, 0, -20),
            "output_filename": "output_bsp_spheres_planes.ppm"
        },
        # Cenário 2: TriMesh (Cenário já existente com Triângulos)
        {
            "spheres": [],
            "planes": [],
            "meshes": [
                TriMesh(
                    1,
                    3,
                    [Point(-1, -1, 5), Point(4, -1, 5), Point(1.5, 4, 5)],
                    [[0, 1, 2]],
                    [Vector(0, 0, -1)],
                    Vector(0.1, 0.1, 0.1), Vector(0.7, 0.2, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100
                ),
                TriMesh(
                    1,
                    3,
                    [Point(0, -3, 6), Point(5, -3, 6), Point(2.5, 2, 6)],
                    [[0, 1, 2]],
                    [Vector(0, 0, -1)],
                    Vector(0.1, 0.1, 0.1), Vector(0.2, 0.7, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100
                )
            ],
            "lights": [LightSource(Point(0, 10, -10), Vector(200, 200, 200))],
            "camera_pos": Point(0, 0, -10),
            "output_filename": "output_bsp_triangles.ppm"
        },
        # Cenário 3: Teste de Divisão BSP com Esferas
        {
            "spheres": [
                Sphere(Point(-3, 0, 10), 2, Vector(0.1, 0.1, 0.1), Vector(0.7, 0.2, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100),
                Sphere(Point(3, 0, 15), 2.5, Vector(0.1, 0.1, 0.1), Vector(0.2, 0.7, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100)
            ],
            "planes": [],
            "meshes": [],
            "lights": [LightSource(Point(0, 10, -10), Vector(200, 200, 200))],
            "camera_pos": Point(0, 0, -20),
            "output_filename": "output_bsp_spheres.ppm"
        },
        # Cenário 4: Teste de Divisão BSP com Plano e Esfera
        {
            "spheres": [
                Sphere(Point(0, 0, 12), 2, Vector(0.1, 0.1, 0.1), Vector(0.7, 0.2, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100)
            ],
            "planes": [
                Plane(Point(0, -3, 10), Vector(0, 1, 0), Vector(0.2, 0.2, 0.2), Vector(0.7, 0.7, 0.7), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1, 10)
            ],
            "meshes": [],
            "lights": [LightSource(Point(0, 10, -10), Vector(200, 200, 200))],
            "camera_pos": Point(0, 0, -20),
            "output_filename": "output_bsp_plane_sphere.ppm"
        },
        # Cenário 5: Intersecting Triangles Large
        {
            "spheres": [],
            "planes": [],
            "meshes": [
                TriMesh(
                    1,
                    3,
                    [Point(-1, -1, 5), Point(4, -1, 5), Point(1.5, 4, 5)],
                    [[0, 1, 2]],
                    [Vector(0, 0, -1)],
                    Vector(0.1, 0.1, 0.1), Vector(0.7, 0.2, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100
                ),
                TriMesh(
                    1,
                    3,
                    [Point(0, -3, 6), Point(5, -3, 6), Point(2.5, 2, 6)],
                    [[0, 1, 2]],
                    [Vector(0, 0, -1)],
                    Vector(0.1, 0.1, 0.1), Vector(0.2, 0.7, 0.2), Vector(1, 1, 1), Vector(0.3, 0.3, 0.3), Vector(0, 0, 0), 1.5, 100
                )
            ],
            "lights": [LightSource(Point(0, 10, -10), Vector(200, 200, 200))],
            "camera_pos": Point(0, 0, -10),
            "output_filename": "intersecting_triangles_large.ppm",
            "resolution": (800, 800)
        }
    ]

    for scenario in scenarios:
        render_scene(
            scenario.get("spheres", []),
            scenario.get("planes", []),
            scenario.get("meshes", []),
            scenario["lights"],
            scenario["camera_pos"],
            scenario["output_filename"],
            scenario.get("resolution", (400, 400))
        )

if __name__ == "__main__":
    main()