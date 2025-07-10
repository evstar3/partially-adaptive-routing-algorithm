`include "src/rcu_header.sv"

module rcu#(
    parameter position_t THIS_POS = '{x:'0, y:'0, z:'0}
) (
    input  logic      clk,
    input  logic      reset,

    input  position_t north_dest_in,
    input  position_t south_dest_in,
    input  position_t east_dest_in,
    input  position_t west_dest_in,
    input  position_t up_dest_in,
    input  position_t down_dest_in,

    input  logic      route_north,
    input  logic      route_south,
    input  logic      route_east,
    input  logic      route_west,
    input  logic      route_up,
    input  logic      route_down,

    input  logic      up_faulty,
    input  logic      down_faulty,

    output port_t     north_dir,
    output port_t     south_dir,
    output port_t     east_dir,
    output port_t     west_dir,
    output port_t     up_dir,
    output port_t     down_dir
);



endmodule
