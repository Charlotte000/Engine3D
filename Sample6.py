import pygame
from opensimplex import OpenSimplex

from Engine3D import Engine
from GeometricShapes import UniformSphere, Sphere
from data.vector import Vector

window = pygame.display.set_mode((500, 500))
engine = Engine(window)

sp = UniformSphere([250, 250, 0], 100, 2000)
sp.point_set(1, '', [100, 100, 100], [0, 0, 255])


gen = OpenSimplex()
for i in sp.points:
	a = Vector.get_copy(i)
	a.remove(Vector(*sp.center))
	a.set_length((gen.noise3d(i[0] / 25, i[1] / 25, i[2] / 25) + 1) * 20)
	i.add(a)

while True:
    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
    		quit()

    window.fill((0, 0, 0))

    sp.rotate_mode()
    engine.draw([sp, True, False, False])

    pygame.display.flip()
    pygame.time.Clock().tick(60)
