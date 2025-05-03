module multilane_fifo#(
    parameter int LANES = 2,
    parameter int DEPTH_BITS = 3,
    parameter int DATA_WIDTH = 32
) (
    input logic clk,
    input logic reset,

    input logic [$clog2(LANES)-1:0] push_lane,
    input logic push,

    input logic [$clog2(LANES)-1:0] pop_lane,
    input logic pop,

    input logic [DATA_WIDTH-1:0] din,

    output logic [DATA_WIDTH-1:0] dout,
    output logic [LANES-1:0] empty,
    output logic [LANES-1:0] full
);

parameter int DEPTH = 2 ** DEPTH_BITS;

logic [LANES-1:0] push_one_hot, pop_one_hot;
assign push_one_hot = {{LANES-1{1'b0}}, push} << push_lane;
assign pop_one_hot  = {{LANES-1{1'b0}}, pop}  << pop_lane;

logic [DATA_WIDTH-1:0] douts [LANES-1:0];

genvar i;
generate
    for (i = 0; i < LANES; i++) begin
        fifo #(
            .DEPTH_BITS(DEPTH_BITS),
            .DATA_WIDTH(DATA_WIDTH)
        ) f0 (
            .clk(clk),
            .reset(reset),
            .push(push_one_hot[i]),
            .pop(pop_one_hot[i]),
            .din(din),
            .dout(douts[i]),
            .empty(empty[i]),
            .full(full[i])
        );
    end
endgenerate

assign dout = douts[pop_lane];

endmodule
