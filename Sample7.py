from Engine3D import Engine
from GeometricShapes import Sphere
import pygame
from opensimplex import OpenSimplex
from data.vector import Vector


b_map = {
	(10, 10, 166):     [-1, -.75],    # Water 3
	(34, 34, 189):     [-.75, -.5],    # Water 2
	(67, 67, 222):     [-.5, -.25],    # Water 1
	(100, 100, 255):     [-.25, 0],    # Water 0

	(255, 255, 100):   [0, .1], # Sand 1
	(235, 235, 80):   [.1, .2], # Sand 0

	(0, 200, 0):     [.2, .35],   # Woodland 1
	(0, 150, 0):     [.35, .55],   # Woodland 0

	(150, 100, 50):    [.55, .65],   # Rock 1
	(100, 50, 0):    [.65, .7],   # Rock 0

	(255, 255, 255): [.7, 1],    # Snow
}

def getColor(value):
	for b in b_map:
		if b_map[b][0] <= value <= b_map[b][1]:
			return b
	return (0, 0, 0)

window = pygame.display.set_mode((600, 600))
engine = Engine(window)
sphere = Sphere([300, 300, 0], 200, 50)
generator = OpenSimplex()

for p in range(len(sphere.points)):
	v = sphere.points[p].copy()
	v -= sphere.center
	n = generator.noise3d(*[i / 100 for i in sphere.points[p][:]]) * 100
	v.setLength(n)
	sphere.points[p] += v

sCol = []
for s in sphere.surfaces:
	v = Vector()
	for i in s:
		v += sphere.points[i]
	v /= len(s)
	v -= sphere.center
	c = (v.length() - 100) / 200 * 2 - 1
	sCol.append(getColor(c))
sphere.surface_set(*sCol)

for p in range(len(sphere.points)):
	v = sphere.points[p].copy()
	v -= sphere.center
	if v.length() < 200:
		v.setLength(200 - v.length())
		sphere.points[p] += v


	
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

	window.fill((0, 0, 0))

	sphere.rotate_mode()

	engine.addToDraw([sphere, False, False, True])
	engine.draw()

	pygame.display.flip()
	pygame.time.Clock().tick(60)

