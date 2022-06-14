from src.graphics import run_example

import pygame, sys
from pygame.locals import *
from math import copysign

from typing import List

import random

epsilon = .00000000001

class Entity:
    def __init__(self, xi, mass=1, v=0, id=None):
        """
        :param x: The initial x position. This variable will not ever be updated over the course of a physics
                  simulation, because really it is just the initial position.
        :param mass:
        :param dx:
        """
        self.xi = xi
        self.mass = mass
        self.v = v
        self.color = [random.randrange(256) for _ in range(3)]
        if id is None:
            self.id = random.randrange(1000)
        else:
            self.id = id

    def position(self, t):
        return self.v * t + self.xi

    def intersect(self, entity):
        return intersect(self, entity)

    def collide(self, entity):
        return collide(self, entity)


def intersect(a: Entity, b: Entity):
    if a.v == b.v:
        return None

    if (b.xi - a.xi) > 0:
        # 'a' is to the left
        if b.v > a.v:
            return None
    else:
        # 'b' is to the left
        if a.v > b.v:
            return None

    t = (b.xi - a.xi) / (a.v - b.v)
    x = a.position(t)

    return t, x


def collide(a: Entity, b: Entity):
    t, x_curr = intersect(a, b)
    # print(a.xi, a.v)
    # print(b.xi, b.v)
    # print(t, x_curr)
    # print(f"---({a.id})({b.id})")

    vaf = ((a.mass - b.mass) / (a.mass + b.mass)) * a.v + ((b.mass + b.mass) / (a.mass + b.mass)) * b.v
    vbf = ((b.mass - a.mass) / (a.mass + b.mass)) * b.v + ((a.mass + a.mass) / (a.mass + b.mass)) * a.v

    a.v = vaf
    a.xi = x_curr - vaf * t

    b.v = vbf
    b.xi = x_curr - vbf * t

    return Collision(t, x_curr, a, b)


def intersects(entities: List[Entity]):
    last_time = -1
    while True:
        results = []
        for a in entities:
            for b in entities:
                if a == b:
                    break
                sect = a.intersect(b)
                # TODO dont return any sects which have already happened
                if sect is not None:
                    # TODO:
                    # this time detection is not perfectly accurate, it's more like a heuristic to eliminate most
                    # redundant collisions
                    if sect[0] <= last_time + epsilon:
                        continue
                    if len(results) == 0:
                        results.append((sect[0], a, b))
                    elif results[0][0] == sect[0]:
                        results.append((sect[0], a, b))
                    elif results[0][0] > sect[0]:
                        results = [(sect[0], a, b)]
        if len(results) == 0:
            return
        for result in results:
            print(f'yielding {result}')
            yield result
        last_time = results[0][0]


class Scene:
    def __init__(self):
        self.entities: List[Entity] = []

    def add(self, entity: Entity):
        self.entities.append(entity)

    def run(self):
        screen_size = (256, 256)
        title = "physics sim"
        bg_color = (0, 0, 0)

        pygame.init()

        display_surf = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(title)

        clock = pygame.time.Clock()

        collision_count = 0

        t = 0
        intersect_iterator = intersects(self.entities)
        try:
            next_sect = next(intersect_iterator)
        except StopIteration:
            next_sect = None
        while True:
            t += clock.tick(30) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # calculate next intersects



            # handle possible collisions
            while next_sect is not None and next_sect[0] <= t:
                collision = next_sect[1].collide(next_sect[2])
                collision_count += 1
                print(f"collision_count={collision_count}")
                print(collision)
                print(next_sect[1], next_sect[2])
                try:
                    next_sect = next(intersect_iterator)
                except StopIteration:
                    next_sect = None




            # for a in self.entities:
            #     for b in self.entities:
            #         if a == b:
            #             break
            #         sect = a.intersect(b)
            #         if sect is not None and t > sect[0]:
            #             print(f'colliding {a.id} and {b.id}')
            #             a.collide(b)

            # clear screen
            display_surf.fill(bg_color)

            # draw objects to screen
            for entity in self.entities:
                pygame.draw.rect(display_surf, entity.color, pygame.Rect(entity.position(t), 50, 5, 5))

            # update screen
            pygame.display.flip()


class Collision:
    """
    TODO: impelement this for better abstraction
    """
    def __init__(self, t, x, a: Entity, b: Entity):
        self.t = t
        self.x = x
        self.entities = (a, b)

    def __str__(self):
        return f"t={self.t}, x={self.x}, ids=({self.entities[0].id}/{self.entities[1].id})"


def example_1():
    scene = Scene()
    a = Entity(50, 1, 30)
    b = Entity(150, 1, 0)
    scene.add(a)
    scene.add(b)
    scene.run()


def example_2():
    scene = Scene()
    for _ in range(10):
        mass = random.randint(50, 100)
        v = random.randrange(-50, 50)
        xi = random.randrange(256)
        scene.add(Entity(xi, mass, v))
    scene.run()


def example_3():
    scene = Scene()
    scene.add(Entity(5, 100000000000000, 0, 1))
    scene.add(Entity(100, 1, 0, 2))
    scene.add(Entity(200, 1000000, -60, 3))
    scene.run()


def main():
    example_3()


if __name__ == "__main__":
    main()
