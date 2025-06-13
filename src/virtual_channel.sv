module virtual_channel#(
    parameter int DEPTH,
    parameter int DATA_WIDTH,
    parameter int VIRTUAL_CHANNELS,

    // internal parameters
    parameter int VC_BITS = $clog2(VIRTUAL_CHANNELS),
    parameter int DEPTH_BITS = $clog2(DEPTH)
) (
    input  logic                  clk,
    input  logic                  reset,
    input  logic                  push,
    input  logic                  pop,
    input  logic [DATA_WIDTH-1:0] flit_in,
    input  logic [           2:0] route_in,
    input  logic [   VC_BITS-1:0] vc_in,

    output logic                  active,
    output logic [DATA_WIDTH-1:0] flit_out,
    output logic [           2:0] route_out,
    output logic [   VC_BITS-1:0] vc_out,
    output logic [  DEPTH_BITS:0] credits
);

fifo#(
    .DEPTH(DEPTH),
    .DATA_WIDTH(DATA_WIDTH)
) fifo0 (
    .clk(clk),
    .reset(reset),
    .push(push),
    .din(flit_in),
    .pop(pop),
    .dout(flit_out),
    .n_free(credits)
);

typedef enum logic [1:0] {
    IDLE,
    ROUTING,
    AWAITING_VC,
    ACTIVE
} vc_state_t;

vc_state_t state, next_state;

logic tail_flit_next; // TODO

always_comb begin
    next_state = state;

    case (state)
        IDLE:
            if (push)
                next_state = ROUTING;
        ROUTING:
            next_state = AWAITING_VC;
        AWAITING_VC:
            next_state = ACTIVE;
        ACTIVE:
            if (pop & tail_flit_next)
                next_state = IDLE;
            // TODO: transition straight to routing
    endcase
end

always_ff @(posedge clk or posedge reset) begin
    if (reset) begin
        route_out <= '0;
        vc_out <= '0;
        state <= IDLE;
    end else begin
        if (state == ROUTING)
            route_out <= route_in;

        if (state == AWAITING_VC)
            vc_out <= vc_in,

        state <= next_state;
    end
end

assign vca_active = state == ACTIVE;

endmodule
