module fifo#(
    parameter int DEPTH_BITS = 3,
    parameter int DATA_WIDTH = 32
) (
    input logic clk,
    input logic reset,

    input logic push,
    input logic pop,
    input logic [DATA_WIDTH-1:0] din,

    output logic [DATA_WIDTH-1:0] dout,
    output logic empty,
    output logic full
);

parameter int DEPTH = 2 ** DEPTH_BITS;

typedef enum logic [1:0] {
    EMPTY = 2'd1,
    FULL  = 2'd2
} state_t;

state_t [1:0] state;
logic [DATA_WIDTH-1:0] regfile [DEPTH-1:0];
logic [DEPTH_BITS:0] read_head, write_head;

always_comb begin
    state = '0;
    if (read_head[DEPTH_BITS-1:0] == write_head[DEPTH_BITS-1:0])
        if (read_head[DEPTH_BITS] ^ write_head[DEPTH_BITS])
            state = FULL;
        else
            state = EMPTY;
end

always_ff @(posedge clk or posedge reset) begin
    if (reset) begin
        read_head <= '0;
        write_head <= '0;
        for (int i = 0; i < DEPTH; i++)
            regfile[i] <= '0;
    end else begin
        case (state)
            EMPTY: begin
                if (push) begin
                    write_head <= write_head + 1;
                    regfile[write_head[DEPTH_BITS-1:0]] <= din;
                end
            end
            FULL: begin
                if (push & pop) begin
                    read_head <= read_head + 1;
                    write_head <= write_head + 1;
                    regfile[write_head[DEPTH_BITS-1:0]] <= din;
                end else if (~push & pop) begin
                    read_head <= read_head + 1;
                end
            end
            default: begin
                if (push & pop) begin
                    read_head <= read_head + 1;
                    write_head <= write_head + 1;
                    regfile[write_head[DEPTH_BITS-1:0]] <= din;
                end else if (push & ~pop) begin
                    write_head <= write_head + 1;
                    regfile[write_head[DEPTH_BITS-1:0]] <= din;
                end else if (~push & pop) begin
                    read_head <= read_head + 1;
                end
            end
        endcase
    end
end

assign empty = state == EMPTY;
assign full  = state == FULL;
assign dout  = regfile[read_head[DEPTH_BITS-1:0]];

endmodule
