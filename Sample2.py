from Engine3D import Engine
from GeometricShapes import Mesh
import pygame

window = pygame.display.set_mode((700, 700))
engine = Engine(window)

mesh = Mesh([350, 350, 0], 300, 10)

# Parameter setting

# Point settings of this object with size: 10px, string: counter, text color: [255, 10, 10] and point colors
# which will alternate
mesh.point_set(10, '_', [255, 10, 10], [0, 0, 0], [255, 0, 255])

# Line settings of this object with size: 10px and line colors which will alternate
mesh.line_set(10, [0, 0, 0], [255, 0, 255])

# Surface settings of this object with the colors that will alternate
mesh.surface_set([0, 0, 0], [255, 0, 255])


# Change the engine.draw settings to see the changes

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    window.fill((91, 91, 91))
    mesh.rotate_mode()

    # Drawing the objects [object, isPoints, isLines, isSurfaces]
    engine.draw([mesh, False, False, True])

    pygame.display.flip()
    pygame.time.Clock().tick(60)
