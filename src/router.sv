module router#(
    // external parameters
    parameter int HEADER_WIDTH = 32,
    parameter int DATA_WIDTH = 32,
    // internal parameters
    parameter int FLIT_WIDTH = HEADER_WIDTH + DATA_WIDTH
) (
    input logic clk,
    input logic reset,

    input logic [FLIT_WIDTH-1:0] west_din,
    input logic [FLIT_WIDTH-1:0] north_din,
    input logic [FLIT_WIDTH-1:0] east_din,
    input logic [FLIT_WIDTH-1:0] south_din,
    input logic [FLIT_WIDTH-1:0] up_din,
    input logic [FLIT_WIDTH-1:0] down_din,

    output logic west_ready,
    output logic north_ready,
    output logic east_ready,
    output logic south_ready,
    output logic up_ready,
    output logic down_ready,

    output logic [FLIT_WIDTH-1:0] west_dout,
    output logic [FLIT_WIDTH-1:0] north_dout,
    output logic [FLIT_WIDTH-1:0] east_dout,
    output logic [FLIT_WIDTH-1:0] south_dout,
    output logic [FLIT_WIDTH-1:0] up_dout,
    output logic [FLIT_WIDTH-1:0] down_dout

    input logic west_dest_ready,
    input logic north_dest_ready,
    input logic east_dest_ready,
    input logic south_dest_ready,
    input logic up_dest_ready,
    input logic down_dest_ready,

);


endmodule
