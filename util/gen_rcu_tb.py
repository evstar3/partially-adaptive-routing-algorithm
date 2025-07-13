#!/usr/bin/python3

from itertools import product
from deadlock import Vector, UnitVector
from math import log2, ceil

def in_bounds(pos, network_size):
    return all((
        pos.z >= 0,
        pos.z < network_size.z,
        pos.y >= 0,
        pos.y < network_size.y,
        pos.x >= 0,
        pos.x < network_size.x
    ))

class Router:
    def __init__(self, x, y, z, network_size):
        self.pos = Vector(x, y, z)
        self.network_size = network_size
        self.network_size_bits = Vector(
            ceil(log2(network_size.x)),
            ceil(log2(network_size.y)),
            ceil(log2(network_size.z))
        )

        self.tag = f'_{x}_{y}_{z}'

        self.name = 'uut' + self.tag
        self.outport = 'outport' + self.tag

    def route(self, dest, inport, up_faulty=False, down_faulty=False):
        vec = dest - self.pos

        if vec.z != 0:
            if vec.z > 0:
                outport = UnitVector.UP
                if not up_faulty:
                    return outport
            elif vec.z < 0:
                outport = UnitVector.DOWN
                if not down_faulty:
                    return outport

            # fault detected
            if inport == UnitVector.EAST:
                # continue the west X sweep, or start the north Y sweep if at the west edge
                if self.pos.x == 0 and self.network_size.y == 1:
                    outdir = UnitVector.DROP
                elif self.pos.x == 0 and self.pos.y == self.network_size.y - 1:
                    outdir = UnitVector.SOUTH
                elif self.pos.x == 0:
                    outdir = UnitVector.NORTH
                else:
                    outdir = UnitVector.WEST
            elif inport == UnitVector.SOUTH:
                # continue the north Y sweep, or start the south Y sweep if at the north edge
                if self.pos.y == self.network_size.y - 1:
                    outdir = UnitVector.SOUTH
                else:
                    outdir = UnitVector.NORTH
            elif inport == UnitVector.NORTH:
                # continue the south Y sweep
                if self.pos.y == 0:
                    outdir = UnitVector.DROP
                else:
                    outdir = UnitVector.SOUTH
            else:
                # start / continue the east X sweep, or go west if at east the edge
                if self.network_size.x == 1 and self.network_size.y == 1:
                    outdir = UnitVector.DROP
                elif self.network_size.x == 1 and self.pos.y == self.network_size.y - 1:
                    outdir = UnitVector.SOUTH
                elif self.network_size.x == 1:
                    outdir = UnitVector.NORTH
                elif self.pos.x == self.network_size.x - 1:
                    outdir = UnitVector.WEST
                else:
                    outdir = UnitVector.EAST

            return outdir

        if vec.x > 0:
            return UnitVector.EAST

        if vec.x < 0:
            return UnitVector.WEST
      
        if vec.y > 0:
            return UnitVector.NORTH

        if vec.y < 0:
            return UnitVector.SOUTH

        return UnitVector.LOCAL

    def decl_str(self):
        return f'''
port_t {self.outport};
rcu#(
    .THIS_POS(position_t'{{{self.network_size_bits.x}'d{self.pos.x}, {self.network_size_bits.y}'d{self.pos.y}, {self.network_size_bits.z}'d{self.pos.z}}})
) {self.name} (
    .inport(inport),
    .dest(dest),
    .up_faulty(up_faulty),
    .down_faulty(down_faulty),
    .outport({self.outport})
);'''
        

def main():
    network_size = Vector(3, 3, 3)
    network_size_bits = Vector(
        ceil(log2(network_size.x)),
        ceil(log2(network_size.y)),
        ceil(log2(network_size.z))
    )

    lines = [
        f'''// THIS CODE WAS AUTOMATICALLY GENERATED

`include "src/rcu_header.sv"
module rcu_tb;
parameter int MESH_WIDTH = {network_size.x};
parameter int MESH_HEIGHT = {network_size.y};
parameter int MESH_DEPTH = {network_size.z};
port_t inport;
position_t dest;
logic up_faulty, down_faulty;'''
    ]

    routers = [Router(x, y, z, network_size) for x, y, z in product(range(network_size.x), range(network_size.y), range(network_size.z))]

    for router in routers:
        lines.append(router.decl_str())

    lines.append('initial begin')
    for inport in UnitVector:
        if inport == UnitVector.DROP:
            continue

        lines.append(f'inport = {inport.name};')

        for up_faulty, down_faulty in product((False, True), (False, True)):
            if inport == UnitVector.UP and up_faulty:
                continue

            if inport == UnitVector.DOWN and down_faulty:
                continue

            lines.append(f'up_faulty = 1\'b{1 if up_faulty else 0};')
            lines.append(f'down_faulty = 1\'b{1 if down_faulty else 0};')
            for dest in routers:
                lines.append(f'dest = \'{{2\'d{dest.pos.x}, 2\'d{dest.pos.y}, 2\'d{dest.pos.z}}};')
                lines.append('#1;')
                for src in routers:
                    if not in_bounds(src.pos + inport.value, network_size):
                        continue

                    expected = src.route(dest.pos, inport, up_faulty=up_faulty, down_faulty=down_faulty)
                    lines.append(f'assert({src.outport} == {expected.name});')

    lines.append('$finish;')
    lines.append('end')
    lines.append('endmodule')

    for line in lines:
        print(line)

if __name__ == '__main__':
    main()
