#!/usr/bin/env python3

import sys
import argparse

from itertools import product
from enum import Enum
from random import random, choice
from time import time, sleep

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def get_edge(edge):
        return edge

    def find_cycle(self):
        for root in self.vertices:
            if cycle := self._find_cycle([], root):
                return cycle

    def _find_cycle(self, history, new_node):
        if new_node in history:
            return history + [new_node]

        for next_node in (edge[1] for edge in self.edges if edge[0] == new_node):
            if cycle := self._find_cycle(history + [new_node], next_node):
                return cycle

        return None

    def strongly_connected(self):
        root = choice(list(self.vertices))

        return self._weakly_connected(root, reverse=False) and self._weakly_connected(root, reverse=True)

    def _weakly_connected(self, root, reverse=False):
        visited = set()

        frontier = [root]

        while frontier:
            current = frontier.pop()

            if current in visited:
                continue

            visited.add(current)

            for src, dst in self.edges:
                if reverse:
                    src, dst = dst, src

                if src == current:
                    frontier.append(dst)

        return visited == self.vertices
    
    def __repr__(self):
        return f'Graph(V={self.vertices}, E={self.edges})'

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

class UnitVector(Enum):
    UP = Vector(0, 0, 1)
    DOWN = Vector(0, 0, -1)
    EAST = Vector(1, 0, 0)
    WEST = Vector(-1, 0, 0)
    NORTH = Vector(0, 1, 0)
    SOUTH = Vector(0, -1, 0)
    LOCAL = Vector(0, 0, 0)
    DROP = None

    def opposite(self):
        return {
            UnitVector.UP: UnitVector.DOWN,
            UnitVector.DOWN: UnitVector.UP,
            UnitVector.EAST: UnitVector.WEST,
            UnitVector.WEST: UnitVector.EAST,
            UnitVector.NORTH: UnitVector.SOUTH,
            UnitVector.SOUTH: UnitVector.NORTH,
        }[self]

class Channel:
    def __init__(self, start: Vector, direction: UnitVector, vc):
        self.start = start
        self.direction = direction
        self.vc = vc

    def end(self):
        return self.start + self.direction.value if self.direction != UnitVector.DROP else None

    def __eq__(self, other):
        return all((self.start == other.start, self.direction == other.direction, self.vc == other.vc))

    def __hash__(self):
        return hash((self.start, self.direction, self.vc))

    def __repr__(self):
        return f'{self.start}--{self.direction.name}:{self.vc}->{self.end()}'

class Network:
    def __init__(self, width, height, depth, fault_rate=0.0):
        self.width = width
        self.height = height
        self.depth = depth
        self.fault_rate = fault_rate

        self.nodes = {Vector(x, y, z) for x, y, z in product(range(width), range(height), range(depth))}

        axes = (
            (UnitVector.UP, UnitVector.DOWN),
            (UnitVector.EAST, UnitVector.WEST),
            (UnitVector.NORTH, UnitVector.SOUTH),
        )

        self.channels = set()
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    channels = [
                        Channel(Vector(x, y, z), UnitVector.EAST, 0),
                        Channel(Vector(x + 1, y, z), UnitVector.WEST, 0),
                        Channel(Vector(x, y, z), UnitVector.NORTH, 0),
                        Channel(Vector(x, y + 1, z), UnitVector.SOUTH, 0),
                    ]

                    if not random() < self.fault_rate:
                        channels += [
                            Channel(Vector(x, y, z), UnitVector.UP, 0),
                            Channel(Vector(x, y, z + 1), UnitVector.DOWN, 0),
                        ]

                    for channel in channels:
                        if channel.end() in self.nodes:
                            self.channels.add(channel)

        self.inet = Graph(self.nodes, {(c.start, c.end()) for c in self.channels})

        self.turns = set()
        for src in self.nodes:
            for dst in self.nodes:
                #print('--BEGIN--')
                #print(src, dst)
                curr_channel = Channel(src, UnitVector.LOCAL, 0)
                #print(curr_channel)
                while True:
                    if curr_channel.direction == UnitVector.LOCAL and curr_channel.end() == dst:
                        break

                    next_channel = self.route_faulty(curr_channel, dst)
                    #print(next_channel)

                    if next_channel.direction == UnitVector.DROP:
                        found_bad_row = False
                        for y in range(self.height):
                            found_good_link = False
                            for x in range(self.width):
                                test_up = Channel(Vector(x, y, 0), UnitVector.UP, 0)
                                test_down = Channel(Vector(x, y, 1), UnitVector.DOWN, 0)
                                assert (test_up in self.channels) == (test_down in self.channels)
                                found_good_link = found_good_link or (test_up in self.channels)
                            found_bad_row = found_bad_row or not found_good_link

                        assert(found_bad_row)
                        raise RuntimeError('Dropping packets, system failure')

                    self.turns.add((curr_channel, next_channel))

                    curr_channel = next_channel

        self.cdg = Graph(self.channels, self.turns)

    def route_faulty(self, channel, dest_node):
        vec = dest_node - channel.end()

        if vec.z != 0:
            if vec.z > 0:
                next_channel = Channel(channel.end(), UnitVector.UP, 0)
            elif vec.z < 0:
                next_channel = Channel(channel.end(), UnitVector.DOWN, 0)

            if next_channel not in self.channels:
                # fault detected
                if self.width == 1:
                    # no where to go, drop the packet
                    next_channel = Channel(channel.end(), UnitVector.DROP, 0)
                elif channel.end().x == self.width - 1:
                    # on the east edge, go west
                    next_channel = Channel(channel.end(), UnitVector.WEST, 0)
                elif channel.direction == UnitVector.WEST and channel.end().x == 0:
                    # on the west edge but we came from the west. the whole row is bad!
                    next_channel = Channel(channel.end(), UnitVector.DROP, 0)
                elif channel.direction == UnitVector.WEST:
                    # heading west but not finding a z-link. keep going west!
                    next_channel = Channel(channel.end(), UnitVector.WEST, 0)
                else:
                    # default to east
                    next_channel = Channel(channel.end(), UnitVector.EAST, 0)

            return next_channel

        if vec.x > 0:
            return Channel(channel.end(), UnitVector.EAST, 0)

        if vec.x < 0:
            return Channel(channel.end(), UnitVector.WEST, 0)
      
        if vec.y > 0:
            return Channel(channel.end(), UnitVector.NORTH, 0)

        if vec.y < 0:
            return Channel(channel.end(), UnitVector.SOUTH, 0)

        return Channel(channel.end(), UnitVector.LOCAL, 0)

    def deadlock_free(self):
        return not self.cdg.find_cycle()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    parser.add_argument('depth', type=int)
    parser.add_argument('-p', '--fault_rate', type=float, required=False, default=0)

    args = parser.parse_args()

    start = time()

    count = 0
    runs = 1000
    for _ in range(runs):
        try:
            ZXY_network = Network(args.width, args.height, args.depth, fault_rate=args.fault_rate)
        except RuntimeError:
            count += 1
    print(count / runs)
    exit(0)

    #print(Channel(Vector(1, 0, 0), UnitVector.UP, 0) in ZXY_network.channels)
    #print(ZXY_network.route(Channel(Vector(1, 0, 0), UnitVector.LOCAL, 0), Vector(1, 0, 1)))
    #print(ZXY_network.route(Channel(Vector(1, 0, 0), UnitVector.WEST, 0), Vector(1, 0, 1)))

    if not ZXY_network.inet.strongly_connected():
        print('not strongly connected')
        exit(1)

    if cycle := ZXY_network.cdg.find_cycle():
        print('not deadlock free')
        print(cycle)
        exit(1)
    
    print(f'{time() - start:.2f}s')

if __name__ == '__main__':
    main()

