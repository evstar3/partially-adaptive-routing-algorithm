`include "router.h"

module rcu#(
    parameter position POS = {0, 0, 0}
) (
    input  logic     clk,
    input  logic     reset,

    input  position  north_dest_in,
    input  position  south_dest_in,
    input  position  east_dest_in,
    input  position  west_dest_in,
    input  position  up_dest_in,
    input  position  down_dest_in,

    input  logic     up_faulty,
    input  logic     down_faulty,

    output direction north_dir,
    output direction south_dir,
    output direction east_dir,
    output direction west_dir,
    output direction up_dir,
    output direction down_dir
);

rcu_single#(
    .POS(POS)
) rcu_north (
    .dest(north_dest_in),
    .dir(north_dir)
);

rcu_single#(
    .POS(POS)
) rcu_south (
    .dest(south_dest_in),
    .dir(south_dir)
);

rcu_single#(
    .POS(POS)
) rcu_east (
    .dest(east_dest_in),
    .dir(east_dir)
);

rcu_single#(
    .POS(POS)
) rcu_west (
    .dest(west_dest_in),
    .dir(west_dir)
);

logic direction up_dir_temp, down_dir_temp;

rcu_single#(
    .POS(POS)
) rcu_up (
    .dest(up_dest_in),
    .dir(up_dir_temp)
);

rcu_single#(
    .POS(POS)
) rcu_down (
    .dest(down_dest_in),
    .dir(down_dir_temp)
);

always_comb begin
    if (up_faulty)
end

endmodule
