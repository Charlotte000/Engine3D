import pygame
from opensimplex import OpenSimplex

from Engine3D import Engine
from GeometricShapes import UniformSphere
from data.vector import Vector

window = pygame.display.set_mode((500, 500))
engine = Engine(window)

sp = UniformSphere([250, 250, 0], 100, 2000)
sp.point_set(1, '', [100, 100, 100], [0, 0, 255])

gen = OpenSimplex()
for i in range(len(sp.points)):
	a = sp.points[i].copy()
	a -= sp.center
	a.setLength((gen.noise3d(sp.points[i][0] / 25, sp.points[i][1] / 25, sp.points[i][2] / 25) + 1) * 20)
	sp.points[i] += a

while True:
    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
    		quit()

    window.fill((0, 0, 0))

    sp.rotate_mode()

    engine.addToDraw([sp, True, False, False])


    engine.draw()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
