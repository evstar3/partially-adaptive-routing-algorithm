module fifo#(
    // external parameters
    parameter int ADDR_WIDTH = 3,
    parameter int DATA_WIDTH = 64,
    // internal parameters
    parameter int DEPTH = 2 ** ADDR_WIDTH
) (
    input logic clk,
    input logic reset,

    input logic push,
    input logic pop,
    input logic [DATA_WIDTH-1:0] din,

    output logic [DATA_WIDTH-1:0] dout;
    output logic empty,
    output logic full
);

typedef enum logic [1:0] {
    EMPTY = 2'd0,
    FULL  = 2'd1,
} state_t;

state_t [1:0] state;
always_comb begin
    if (n_elements == 0)
        state = EMPTY;
    else if (n_elements == DEPTH)
        state = FULL;
end

logic [DATA_WIDTH-1:0] regfile [DEPTH-1:0];
logic [ADDR_WIDTH-1:0] n_elements, read_head, write_head;
always_ff @(posedge clk or posedge reset) begin
    if (reset) begin
        n_elements <= '0;
        read_head <= '0;
        write_head <= '0;
        for (int i = 0; i < DEPTH; i++)
            regfile[i] <= '0;
    end else begin
        case (state)
            EMPTY: begin
                if (push) begin
                    write_head <= write_head + 1;
                    regfile[write_head] <= din;
                    n_elements <= n_elements + 1;
                end
            end
            FULL: begin
                if (pop) begin
                    read_head <= read_head + 1;
                    if (push) begin
                        write_head <= write_head + 1;
                        regfile[write_head] <= din;
                    end else
                        n_elements <= n_elements - 1;
                end
            end
            default: begin
                if (push & pop) begin
                    read_head <= read_head + 1;
                    write_head <= write_head + 1;
                    regfile[write_head] <= din;
                end else if (push & ~pop) begin
                    write_head <= write_head + 1;
                    regfile[write_head] <= din;
                    n_elements <= n_elements + 1;
                end else if (~push & pop) begin
                    read_head <= read_head + 1;
                    n_elements <= n_elements - 1;
                end
            end
        endcase
    end
end

assign empty = state == EMPTY;
assign full  = state == FULL;
assign dout = regfile[read_head];

endmodule



