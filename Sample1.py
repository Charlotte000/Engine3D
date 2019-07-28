from Engine3D import Engine
from GeometricShapes import Mesh
import pygame

# Creating PyGame Surface
window = pygame.display.set_mode((700, 700))

# Creating Engine3D object with the pygame surface
engine = Engine(window)

# Creating Mesh in position [250, 250, 0] and size 300px and 10 cells each side
mesh = Mesh([350, 350, 0], 300, 10)

while True:
    # PyGame key event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # Filling the screen
    window.fill((91, 91, 91))

    # Setting rotation mode by the mouse on this object
    mesh.rotate_mode()

    # Drawing the objects [object, isPoints, isLines, isSurfaces]
    engine.draw([mesh, True, True, True])

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)
