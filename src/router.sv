module router#(
    parameter int DEPTH,
    parameter int DATA_WIDTH,
    parameter int VIRTUAL_CHANNELS,
    parameter int NOC_WIDTH,
    parameter int NOC_DEPTH,
    parameter int NOC_HEIGHT,

    // internal parameters
    parameter int VC_BITS = $clog2(VIRTUAL_CHANNELS),
    parameter int NOC_ADDR_BITS = $clog2(NOC_WIDTH) + $clog2(NOC_DEPTH) + $clog2(NOC_HEIGHT),
    parameter int DEPTH_BITS = $clog2(DEPTH)
) (
    input  logic                  clk,
    input  logic                  reset,
    input  logic                  push     [2:0],
    input  logic [DATA_WIDTH-1:0] flit_in  [2:0],
    input  logic [   VC_BITS-1:0] vc_in    [2:0],

    output logic                  pop      [2:0],
    output logic [DATA_WIDTH-1:0] flit_out [2:0],
    output logic [   VC_BITS-1:0] vc_out   [2:0],
    output logic [  DEPTH_BITS:0] credits  [VIRTUAL_CHANNELS-1:0] [2:0]
);

logic [VIRTUAL_CHANNELS-1:0] active [2:0]; // needed for switch allocator

genvar i;
generate
    for (int i = 0; i < 6; i++) begin
        input_buffer#(
            .DEPTH(DEPTH),
            .DATA_WIDTH(DATA_WIDTH),
            .VIRTUAL_CHANNELS(VIRTUAL_CHANNELS),
            .NOC_WIDTH(NOC_WIDTH),
            .NOC_DEPTH(NOC_DEPTH),
            .NOC_HEIGHT(NOC_HEIGHT)
        ) ib (
            .clk(clk),
            .reset(reset),
            .push(push),
            .pop(pop),
            .push_lane(vc_in),
            .pop_lane(), //TODO
            .flit_in(flit_in),
            .route_in(), //TODO
            .vc_in(), //TODO
            .need_route(), //TODO
            .need_vc(), //TODO,
            .active(active[i]),
            .dest_addr(), //TODO,
            .flit_out(), //TODO
            .route_out(), //TODO
            .vc_out(), //TODO
            .credits(credits[i])
        );
    end
endgenerate

/*

Pipeline stages:
    SA - switch allocation
        Switch allocator awards grants to flits in active VCs.
        Flits and output VCs are popped from input buffers and buffered in a pipeline register just before the switch.
        Switch configuration is buffered in pipeline register
    ST - switch traversal
        Switch is configured via pipeline registers
        Flits and output VCs traverse the switch
        Flits and output VCs captured after switch and before link
    LT - link traversal
        Flits and output VCs exit the router

*/

endmodule
