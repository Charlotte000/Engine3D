# Engine3D
Python 3D engine

My python 3D engine includes rotation the shapes, its projection to the PyGame Surface, kinds of geometrical shapes, color settings.


## Usage

Importing all needed libraries:
```python
import pygame                       # Importing PyGame
from Engine3D import Engine         # Importing 3D Engine
from GeometricShapes import Mesh    # Importing Mesh-Object
```

First we should create a *pygame Surface* object as a display:
```python
screen = pygame.display.set_mode((700, 700))
```

Creating an engine instance:
```python
engine3d = Engine(screen)
```
Creating a mesh as an object. Arguments are: position [x, y, z], size, cells count in a row
```python
mesh = Mesh([350, 350, 0], 300, 10)
```

Creating an infinite loop:
```python
while True:
```

Setting a rotation mode of the mesh:
```python
mesh.rotate_mode()
```

Drawing our object:
```python
engine3d.draw([mesh, True, True, True])
```

Updating screen using *PyGame*:
```python
pygame.display.flip()
```


