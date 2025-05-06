module fifo#(
    parameter int DEPTH = 3,
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

parameter int DEPTH_BITS = $clog2(DEPTH);

typedef enum logic [1:0] {
    EMPTY = 2'd1,
    FULL  = 2'd2
} state_t;

state_t [1:0] state;

logic [DEPTH_BITS:0] n_elements;
always_comb begin
    state = '0;
    if (n_elements == 0)
        state = EMPTY;
    else if (n_elements == DEPTH)
        state = FULL;
end

logic do_read, do_write;
always_comb begin
    do_read  = 1'b0;
    do_write = 1'b0;

    case (state)
        EMPTY: begin
            do_write = push;
        end
        FULL: begin
            do_read = pop;
            do_write = push & pop;
        end
        default: begin
            do_read = pop;
            do_write = push;
        end
    endcase
end

logic [DEPTH_BITS-1:0] read_head, write_head;
logic [DEPTH_BITS-1:0] read_head_next, write_head_next;
always_comb begin
    read_head_next  = read_head  == DEPTH - 1 ? '0 : read_head  + 1;
    write_head_next = write_head == DEPTH - 1 ? '0 : write_head + 1;
end

logic [DATA_WIDTH-1:0] regfile [DEPTH-1:0];
always_ff @(posedge clk or posedge reset) begin
    if (reset) begin
        read_head <= '0;
        write_head <= '0;
        n_elements <= '0;
        for (int i = 0; i < DEPTH; i++)
            regfile[i] <= '0;
    end else begin
        if (do_read)
            read_head <= read_head_next;

        if (do_write) begin
            regfile[write_head] <= din;
            write_head <= write_head_next;
        end

        if (do_read & ~do_write)
            n_elements = n_elements - 1;
        else if (~do_read & do_write)
            n_elements = n_elements + 1;
    end
end

assign empty = state == EMPTY;
assign full  = state == FULL;
assign dout  = regfile[read_head];

endmodule

