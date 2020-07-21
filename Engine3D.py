from data.vector import Vector
from math import sin, cos
import pygame


class Object3D:
    def __init__(self, center: [float, float, float]):
        self.center = Vector(*center)
        self.rotate_point = Vector(*center)

        # Angle
        self.angle = Vector()
        self.danglex = self.dangley = 0

        # Move figure
        for i in range(len(self.points)):
            self.points[i] += self.center

        # Drawing settings
        self.point_settings = [[(255, 0, 0)], 7, '', (255, 0, 255)]
        self.line_settings = [[(0, 255, 0)], 5]
        self.surface_settings = [(0, 0, 255)]

    def rotate(self, dx: float, dy: float, dz: float) -> None:
        self.angle += Vector(dx, dy, dz)
        Engine.rotate(self.points, self.rotate_point, dx, dy, dz)

    def point_set(self, size: int, text: str, text_color: [int, int, int], *colors: [int, int, int]) -> None:
        """
        Changes settings of point
        size: Point size
        text: Text under the point, if '_' - point counter
        text_color: [r, g, b] color of text
        colors: [r, g, b] color of the point
        """
        self.point_settings = [colors, size, text, text_color]

    def line_set(self, width: int, *colors: [int, int, int]) -> None:
        """
        Changes settings of line
        width: Line width
        colors: [r, g, b] color of the line
        """
        self.line_settings = [colors, width]

    def surface_set(self, *colors: [int, int, int]) -> None:
        """
        Changes settings of surface
        colors: [r, g, b] color of the surface
        """
        self.surface_settings = colors

    def rotate_mode(self) -> None:
        if pygame.mouse.get_pressed()[0]:
            self.dangley, self.danglex = pygame.mouse.get_rel()
            self.danglex /= -400
            self.dangley /= 400
        pygame.mouse.get_rel()

        self.danglex *= .99
        self.dangley *= .99

        self.rotate(self.danglex, self.dangley, 0)



class Engine:
    def __init__(self, screen: pygame.Surface):
        pygame.font.init()
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 30)
        self.toDraw = []

    
    def addToDraw(self, *items: list) -> None:
        """
        Add to draw one or more items. 
        Use engine.draw() to blit them.
        Items is a list of [figure: Object3D, is_points: bool, is_lines: bool, is_surfaces: bool]
        """
        self.toDraw.extend(items)


    def draw(self) -> None:
        """
        Draws items on the screen
        """

        # Collecting to_blit
        to_blit = []
        for item in self.toDraw:
            if item[1]:
                to_blit.extend([['point', [i], item[0].point_settings[0][c % len(item[0].point_settings[0])],
                                 item[0].point_settings[1], self.font,
                                 item[0].point_settings[2] if item[0].point_settings[2] != '_' else c,
                                 item[0].point_settings[3]] for c, i in enumerate(item[0].points)])
            if item[2]:
                to_blit.extend([['line', [item[0].points[i[0]], item[0].points[i[1]]],
                                 item[0].line_settings[0][c % len(item[0].line_settings[0])],
                                 item[0].line_settings[1]] for c, i in enumerate(item[0].lines)])
            if item[3]:
                to_blit.extend([['surface', [item[0].points[i] for i in num],
                                 item[0].surface_settings[c % len(item[0].surface_settings)]]
                                for c, num in enumerate(item[0].surfaces)])

        # Sorting to_blit by depth
        to_blit = sorted(to_blit, key=lambda unit: sum([i[2] for i in unit[1]]) / len(unit[1]))

        # Drawing
        for unit in to_blit:
            if unit[0] == 'point':
                Engine.draw_point(unit[1][0], unit[2], self.screen, unit[3], unit[4], unit[5], unit[6])
            if unit[0] == 'line':
                Engine.draw_line(unit[1], unit[2], self.screen, unit[3])
            if unit[0] == 'surface':
                Engine.draw_surface(unit[1], unit[2], self.screen)

        # Clear toDraw list
        self.toDraw = []

    def draw_depth_map(self, *items: [Object3D, bool, bool, bool]) -> None:
        """
        Draws items with depth map. 
        Items is a list of [figure, is_points, is_lines, is_surfaces]
        """

        def round_depth(surface_depth):
            array = [p[2] for p in surface_depth]
            return sum(array) / len(array)

        # Collecting to_blit
        to_blit = []
        for item in items:
            to_blit.extend([item.points[i].copy() for i in s] for s in item.surfaces)

        # Sorting by depth
        to_blit = sorted(to_blit, key=lambda surf: round_depth(surf))

        # Depth range
        minlen = round_depth(to_blit[0])
        maxlen = round_depth(to_blit[-1])

        if minlen == maxlen == 0:
            maxlen = 0
            minlen = 1
        maxlen -= minlen

        # Drawing
        for surface in to_blit:
            current_len = round_depth(surface) - minlen
            col = current_len / maxlen * 255
            projected = [point[:2] for point in Engine.get_projection(surface)]
            pygame.draw.polygon(self.screen, (col, col, col), projected)

    @staticmethod
    def draw_surface(points: [Vector], color: [int, int, int], surf: pygame.Surface) -> None:
        projected = [i[:2] for i in Engine.get_projection(points)]
        pygame.draw.polygon(surf, color, projected)

    @staticmethod
    def draw_line(points: [Vector], color: [int, int, int], surf: pygame.Surface, width: int =1) -> None:
        projected = [i[:2] for i in Engine.get_projection(points)]
        pygame.draw.line(surf, color, projected[0], projected[1], width)

    @staticmethod
    def draw_point(point: Vector, color: [int, int, int], surf: pygame.Surface, radius: int, font: pygame.font, text: str, text_color: [int, int, int]) -> None:
        projected = Engine.get_projection([point])[0][:]
        if radius > 1:
            pygame.draw.circle(surf, color, (round(projected[0]), round(projected[1])), radius)
        else:
            surf.set_at((round(projected[0]), round(projected[1])), color)
        if text != '':
            surf.blit(font.render(str(text), True, text_color), (round(projected[0]), round(projected[1])))

    @staticmethod
    def rotate(figure: [Vector], rotate_point: Vector, angleX: float, angleY: float, angleZ: float) -> [Vector]:
        for p in range(len(figure)):
            figure[p] -= Vector(*rotate_point)

        rotationX = [
            [1, 0, 0],
            [0, cos(angleX), -sin(angleX)],
            [0, sin(angleX), cos(angleX)]
        ]
        rotationY = [
            [cos(angleY), 0, sin(angleY)],
            [0, 1, 0],
            [-sin(angleY), 0, cos(angleY)]
        ]
        rotationZ = [
            [cos(angleZ), -sin(angleZ), 0],
            [sin(angleZ), cos(angleZ), 0],
            [0, 0, 1]
        ]
        for i in range(len(figure)):
            for rot in [rotationX, rotationY, rotationZ]:
                figure[i] = Engine.matrix_mult(rot, figure[i])
        for p in range(len(figure)):
            figure[p] += Vector(*rotate_point)
        return figure

    @staticmethod
    def matrix_mult(a: list, v: Vector) -> Vector:
        b = v[0], v[1], v[2]
        result = []
        for ay in range(len(a)):
            result.append(sum([a[ay][bx] * b[bx] for bx in range(len(b))]))
        return Vector(*result)

    @staticmethod
    def get_projection(figure: [Vector]) -> list:
        projected_points = []
        for c in figure:
            projection = [
                [1, 0, 0],
                [0, 1, 0]
            ]
            p = Engine.matrix_mult(projection, c)
            projected_points.append(p)
        return projected_points
