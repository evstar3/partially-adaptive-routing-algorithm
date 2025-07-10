`ifndef RCU_HEADER
`define RCU_HEADER

parameter int MESH_WIDTH  = 4;
parameter int MESH_HEIGHT = 4;
parameter int MESH_DEPTH  = 2;

typedef struct {
    logic [$clog2(MESH_WIDTH)-1:0] x;
    logic [$clog2(MESH_HEIGHT)-1:0] y;
    logic [$clog2(MESH_DEPTH)-1:0] z;
} position_t;

typedef enum logic [2:0] {
    LOCAL = 3'd0,
    NORTH = 3'd1,
    SOUTH = 3'd2,
    EAST  = 3'd3,
    WEST  = 3'd4,
    UP    = 3'd5,
    DOWN  = 3'd6
} port_t;

`endif
