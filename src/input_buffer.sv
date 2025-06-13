module input_buffer#(
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
    input  logic                        clk,
    input  logic                        reset,
    input  logic                        push,
    input  logic                        pop,
    input  logic [         VC_BITS-1:0] push_lane,
    input  logic [         VC_BITS-1:0] pop_lane,
    input  logic [      DATA_WIDTH-1:0] flit_in,
    input  logic [                 2:0] route_in,
    input  logic [         VC_BITS-1:0] vc_in,

    output logic                        need_route,
    output logic                        need_vc,
    output logic [VIRTUAL_CHANNELS-1:0] active,
    output logic [   NOC_ADDR_BITS-1:0] dest_addr,
    output logic [      DATA_WIDTH-1:0] flit_out,
    output logic [                 2:0] route_out [VIRTUAL_CHANNELS-1:0],
    output logic [         VC_BITS-1:0] vc_out    [VIRTUAL_CHANNELS-1:0],
    output logic [        DEPTH_BITS:0] credits   [VIRTUAL_CHANNELS-1:0]
);

logic [VIRTUAL_CHANNELS-1:0] push_one_hot, pop_one_hot;
assign push_one_hot = push << push_lane;
assign pop_one_hot = pop << pop_lane;

logic [DATA_WIDTH-1:0] flit_outs [VIRTUAL_CHANNELS-1:0];

genvar i;
generate
    for (i = 0; i < VIRTUAL_CHANNELS; i++) begin
        virtual_channel#(
            .DEPTH(DEPTH),
            .DATA_WIDTH(DATA_WIDTH),
            .VIRTUAL_CHANNELS(VIRTUAL_CHANNELS)
        ) vc (
            .clk(clk),
            .reset(reset),
            .push(push_one_hot[i]),
            .pop(pop_one_hot[i]),
            .flit_in(flit_in),
            .route_in(route_in),
            .vc_in(vc_in),
            .active(active[i]),
            .flit_out(flit_outs[i]),
            .route_out(route_out[i]),
            .vc_out(vc_outs[i]),
            .credits(credits[i])
        );
    end
endgenerate

/*

Pipeline stages:
    BW - Buffer Write
        Flit moves from link into its virtual channel FIFO
    RC - Route Computation
        Flit chills in FIFO
        Router gets flit destination and responds with an output port
    VA - Virtual Channel Allocation
        Flit chills in FIFO
        VC allocator gets 

*/

logic [VC_BITS-1:0] BW_RC_vc;
logic               BW_RC_is_head;
always_ff @(posedge clk or posedge reset) begin
    if (reset | ~|push) begin
        BW_RC_vc <= '0;
        BW_RC_is_head <= '0;
        dest_addr <= '0;
    end else begin
        BW_RC_vc <= din_vc;
        BW_RC_is_head <= |(push & available); // TODO
        dest_addr <= din[0:0]; // TODO
    end
end

logic [VC_BITS-1:0] RC_VA_vc;
logic               RC_VA_is_head;
always_ff @(posedge clk or posedge reset) begin
    if (reset | ~BW_RC_is_head) begin
        RC_VA_vc <= '0;
        RC_VA_is_head <= '0;
    end else begin
        RC_VA_vc <= BW_RC_vc;
        RC_VA_is_head <= BW_RC_is_head;
    end
end

assign need_route = BW_RC_is_head;
assign need_vc    = RC_VA_is_head;

assign flit_out = flit_outs[pop_lane];

endmodule
