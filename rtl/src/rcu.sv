`include "src/rcu_header.sv"

module rcu#(
    parameter position_t THIS_POS = '{x:'0, y:'0, z:'0}
) (
    input  port_t      inport,
    input  position_t  dest,
    input  logic       up_faulty,
    input  logic       down_faulty,

    output port_t      outport
);

typedef enum logic [1:0] {
    ZERO = 2'd0,
    POS  = 2'd1,
    NEG  = 2'd3
} direction_t;

logic [$clog2(MESH_DEPTH):0] z_hops;
assign z_hops = {1'b0, dest.z} - {1'b0, THIS_POS.z};
assign z_dir  = {2{z_hops[$clog2(MESH_DEPTH)]}} | {1'b0, |z_hops[$clog2(MESH_DEPTH)-1:0]};

logic [$clog2(MESH_WIDTH):0] x_hops;
assign x_hops = {1'b0, dest.X} - {1'b0, THIS_POS.x};
assign x_dir  = {2{x_hops[$clog2(MESH_WIDTH)]}} | {1'b0, |x_hops[$clog2(MESH_WIDTH)-1:0]};

logic [$clog2(MESH_HEIGHT):0] y_hops;
assign y_hops = {1'b0, dest.y} - {1'b0, THIS_POS.y};
assign y_dir  = {2{y_hops[$clog2(MESH_HEIGHT)]}} | {1'b0, |y_hops[$clog2(MESH_HEIGHT)-1:0]};

logic x_sel;
port_t backup;

logic this_east_edge, this_west_edge, this_north_edge, this_south_edge;
assign this_east_edge = THIS.x == MESH_WIDTH - 1;
assign this_west_edge = THIS.x == 0;
assign this_north_edge = THIS.y == MESH_HEIGHT - 1;
assign this_south_edge = THIS.y == 0;

always_comb begin
    // select the backup direction
    if (inport == EAST) begin
        if (this_west_edge && MESH_HEIGHT == 1)
            backup = DROP;
        else if (this_west_edge && this_north_edge)
            backup = SOUTH;
        else if (this_west_edge)
            backup = NORTH;
        else
            backup = WEST;
    end else if (inport == SOUTH) begin
        if (this_north_edge)
            backup = SOUTH;
        else
            backup = NORTH;
    end else if (inport == NORTH) begin
        if (this_south_edge)
            backup = DROP;
        else
            backup = SOUTH;
    end else begin
        if (MESH_WIDTH == 1 && MESH_HEIGHT == 1)
            backup = DROP;
        else if (this_north_edge && MESH_WIDTH == 1)
            backup = SOUTH;
        else if (MESH_WIDTH == 1)
            backup = NORTH;
        else if (this_east_edge)
            backup = WEST;
        else
            backup = EAST;
    end


    if (z_dir != ZERO) begin
        if (z_dir == POS && up_faulty || z_dir == NEG && down_faulty)
            // use the random backup x direction
            outport = backup;
        else
            outport = z_dir == POS ? UP : DOWN;
    end else if (x_dir != ZERO)
        outport = x_dir == POS ? EAST : WEST;
    else if (y_dir != ZERO)
        outport = y_dir == POS ? NORTH : SOUTH;
    else
        outport = LOCAL;
end


endmodule
