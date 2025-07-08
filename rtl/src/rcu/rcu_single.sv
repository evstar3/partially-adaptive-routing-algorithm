`include "rcu.h"

module rcu_single#(
    parameter position POS = {0, 0, 0}
) (
    input  position  dest,
    output direction dir
);

always_comb begin
    dir = LOCAL;

    if (destination.z > POS.z)
        dir = UP;
    else if (destination.z < POS.z)
        dir = DOWN;
    else if (destination.x > POS.x)
        dir = EAST;
    else if (destination.x < POS.x)
        dir = WEST;
    else if (destination.y > POS.y)
        dir = NORTH;
    else if (destination.y < POS.y)
        dir = SOUTH;
    else
        dir = LOCAL;
end

endmodule
