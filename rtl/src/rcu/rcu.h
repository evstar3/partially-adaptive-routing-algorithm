`define MESH_WIDTH 4
`define MESH_HEIGHT 4
`define MESH_DEPTH 2

struct {
    logic [$clog2(MESH_WIDTH)-1:0] x;
    logic [$clog2(MESH_HEIGHT)-1:0] y;
    logic [$clog2(MESH_DEPTH)-1:0] z;
} position;

enum logic [2:0] {
    LOCAL,
    NORTH,
    SOUTH,
    EAST,
    WEST,
    UP,
    DOWN
} direction;
