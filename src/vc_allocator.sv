`include "flit.sv"

module vc_allocator#(
    parameter int LANES_PER_CHANNEL = 2,
    parameter int VC_DEPTH = 5,
    parameter int FLIT_SIZE = 32
) (
    input clk,
    input reset,

    input logic [FLIT_SIZE-1:0] din0,
    input logic [FLIT_SIZE-1:0] din1,
    input logic [FLIT_SIZE-1:0] din2,
    input logic [FLIT_SIZE-1:0] din3,
    input logic [FLIT_SIZE-1:0] din4,
    input logic [FLIT_SIZE-1:0] din5,

    input logic din0_valid,
    input logic din1_valid,
    input logic din2_valid,
    input logic din3_valid,
    input logic din4_valid,
    input logic din5_valid
)

endmodule
