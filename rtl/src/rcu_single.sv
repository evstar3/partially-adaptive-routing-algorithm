`include "src/rcu_header.sv"

module rcu_single#(
    parameter position_t THIS_POS = '{x:'0, y:'0, z:'0}
) (
    input  port_t      inport,
    input  position_t  dest,
    input  logic       up_faulty,
    input  logic       down_faulty,
    input  logic       rand_bit,

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
port_t backup_direction;

always_comb begin
    // select the backup direction
    if (THIS_POS.x == MESH_WIDTH - 1)
        backup_direction = WEST;
    else if (inport == EAST)
        backup_direction = THIS_POS.x == 0 ? DROP : WEST;
    else
        backup_direction = EAST;

    if (z_dir != ZERO) begin
        if (z_dir == POS && up_faulty || z_dir == NEG && down_faulty)
            // use the random backup x direction
            outport = backup_direction;
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
