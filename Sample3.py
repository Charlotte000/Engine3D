from Engine3D import Engine
from GeometricShapes import Mesh
import pygame

window = pygame.display.set_mode((700, 700))
engine = Engine(window)

mesh = Mesh([350, 350, 0], 300, 10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    window.fill((91, 91, 91))
    mesh.rotate_mode()

    # Drawing the objects with its depth map. The further surfaces are the darker its color
    engine.draw_depth_map(mesh)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
