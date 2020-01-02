from Engine3D import Engine
import pygame
from GeometricShapes import MobiusStrip

window = pygame.display.set_mode((700, 700))
engine = Engine(window)

m = MobiusStrip([350, 350, 0], 100, 10)
m.surface_set([0, 0, 0], [255, 0, 255])
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    window.fill((91, 91, 91))

    m.rotate_mode()
    engine.addToDraw([m, False, False, True])

    engine.draw()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
