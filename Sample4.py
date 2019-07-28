from Engine3D import Engine
import pygame
from data.vector import Vector

window = pygame.display.set_mode((700, 700))
engine = Engine(window)

# Create your own shapes
points = [Vector(300, 300, 0), Vector(400, 300, 0), Vector(400, 400, 0), Vector(300, 400, 0)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    window.fill((91, 91, 91))

    # Draws a simple surface that bounded by points with the color [255, 100, 100] on the window
    engine.draw_surface(points, [255, 100, 100], window)

    # Rotate the shape of points with the rotate point [300, 300, 0] .005, .005, -.001 degrees on axes OX, OY, OZ
    engine.rotate(points, [300, 300, 0], .005, .005, -.001)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
