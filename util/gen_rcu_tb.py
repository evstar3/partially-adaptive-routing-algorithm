#!/usr/bin/python3

from itertools import product
from enum import Enum

from deadlock import Vector, UnitVector, Network

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return all((self.x == other.x, self.y == other.y, self.z == other.z))

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def in_bounds(self, bounds):
        return all((
            self.x >= 0,
            self.x < bounds.x,
            self.y >= 0,
            self.y < bounds.y,
            self.z >= 0,
            self.z < bounds.z,
        ))

    def set_dest_str(self):
        return f'dest = \'{{2\'d{self.x}, 2\'d{self.y}, 2\'d{self.z}}};'

UP = Vector(0, 0, 1)
DOWN = Vector(0, 0, -1)
EAST = Vector(1, 0, 0)
WEST = Vector(-1, 0, 0)
NORTH = Vector(0, 1, 0)
SOUTH = Vector(0, -1, 0)
LOCAL = Vector(0, 0, 0)
DROP = None

class Router:
    def __init__(self, x, y, z, bounds):
        self.pos = Vector(x, y, z)
        self.bounds = bounds

        self.tag = f'_{x}_{y}_{z}'

        self.router_name = 'uut' + self.tag
        self.outport_name = 'outport' + self.tag

    def get_dest(self, dest, up_faulty, down_faulty):
        offsets = (-1, 0, 1)

        for x, y, z in product(offsets, offsets, offsets):
            dest = self.pos + Vector(x, y, z)
            if not dest.in_bounds(self.bounds):
                continue

            if z > 0:
                expected = 'UP'
            elif z < 0:
                expected = 'DOWN'
            elif x > 0:
                expected = 'EAST'
            elif x < 0:
                expected = 'WEST'
            elif y > 0:
                expected = 'NORTH'
            elif y < 0:
                expected = 'SOUTH'
            else:
                expected = 'LOCAL'

            return [
                dest.set_dest_str(),
                '#1;',
                f'assert(outport == {expected});'
            ]

def main():
    size = 3
    bounds = Vector(size, size, size)
    for x, y, z in product(range(size), range(size), range(size)):
        print(Router(x, y, z, bounds).normal_tests_strs())

if __name__ == '__main__':
    main()
