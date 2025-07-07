#!/usr/bin/env python3

from enum import Enum, auto

class Direction(Enum):
    PLUS_X = auto()
    MINUS_X = auto()
    PLUS_Y = auto()
    MINUS_Y = auto()
    PLUS_Z = auto()
    MINUS_Z = auto()

STANDARD_ROUTES = {
    Direction.PLUS_X: [Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.MINUS_X: [Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.PLUS_Y: [],
    Direction.MINUS_Y: [],
    Direction.PLUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.MINUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y]
}

CYCLIC_ROUTES = {
    Direction.PLUS_X: [Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.MINUS_X: [Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.PLUS_Y: [Direction.PLUS_X],
    Direction.MINUS_Y: [Direction.MINUS_X],
    Direction.PLUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.MINUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y]
}

NEW_ROUTES = {
    Direction.PLUS_X: [Direction.PLUS_Y, Direction.MINUS_Y, Direction.PLUS_Z, Direction.MINUS_Z],
    Direction.MINUS_X: [Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.PLUS_Y: [Direction.PLUS_Z, Direction.MINUS_Z],
    Direction.MINUS_Y: [],
    Direction.PLUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.MINUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y]
}

NEW_ROUTES_2 = {
    Direction.PLUS_X: [Direction.PLUS_Y, Direction.MINUS_Y, Direction.PLUS_Z, Direction.MINUS_Z],
    Direction.MINUS_X: [Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.PLUS_Y: [],
    Direction.MINUS_Y: [],
    Direction.PLUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.MINUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y]
}

NEW_ROUTES_3 = {
    Direction.PLUS_X: [Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.MINUS_X: [Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.PLUS_Y: [Direction.PLUS_Z, Direction.MINUS_Z],
    Direction.MINUS_Y: [],
    Direction.PLUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y],
    Direction.MINUS_Z: [Direction.PLUS_X, Direction.MINUS_X, Direction.PLUS_Y, Direction.MINUS_Y]
}

class Node:
    def __init__(self, direction):
        self.direction = direction
        self.children = []

    def add_children(self):
        self.children = [Node(direction) for direction in self.Routes[self.direction]] 

    def __repr__(self):
        return str(self.direction)

class Tree:
    Opposites = {
        Direction.PLUS_X: Direction.MINUS_X,
        Direction.MINUS_X: Direction.PLUS_X,
        Direction.PLUS_Y: Direction.MINUS_Y,
        Direction.MINUS_Y: Direction.PLUS_Y,
        Direction.PLUS_Z: Direction.MINUS_Z,
        Direction.MINUS_Z: Direction.PLUS_Z
    }

    def __init__(self, routes):
        self.Node = Node
        self.Node.Routes = routes

        self.roots = [Node(direction) for direction in self.Node.Routes]

    def cycle_exists(self):
        return any(self._cycle_exists([direction]) for direction in self.roots)

    def _cycle_exists(self, curr_path):
        start_node = curr_path[0]
        end_node   = curr_path[-1]

        directions = [node.direction for node in curr_path[:-1]]

        # detect loop
        if end_node.direction in directions:
            if self.Opposites[start_node.direction] in directions and start_node.direction == end_node.direction:
                print(curr_path)
                return True
            else:
                return False

        end_node.add_children()
        return any(self._cycle_exists(curr_path + [child]) for child in end_node.children)

def main():
    for routes in (STANDARD_ROUTES, CYCLIC_ROUTES, NEW_ROUTES, NEW_ROUTES_2, NEW_ROUTES_3):
        print(Tree(routes).cycle_exists())

if __name__ == '__main__':
    main()
