module fifo_tb;

parameter int ADDR_WIDTH = 3;
parameter int DATA_WIDTH = 32;
parameter int DEPTH = 2 ** ADDR_WIDTH;

logic clk, reset;
logic push, pop;
logic empty, full;
logic [DATA_WIDTH-1:0] din, dout;

fifo #(
    .ADDR_WIDTH(ADDR_WIDTH),
    .DATA_WIDTH(DATA_WIDTH)
) dut (
    .clk(clk),
    .reset(reset),
    .push(push),
    .pop(pop),
    .din(din),
    .dout(dout),
    .empty(empty),
    .full(full)
);

initial begin
    clk = 1'b0;
    forever #5 clk = ~clk;
end

int i;
initial begin
    push = 1'b0;
    pop = 1'b0;
    reset = 1'b1;
    #10;
    reset = 1'b0;

    assert(empty == 1'b1);

    for (i = 0; i < DEPTH; i++) begin
        push = 1'b1;
        pop = 1'b0;
        din = i;
        assert(full == 1'b0);
        #10;
        assert(empty == 1'b0);
    end

    assert(full == 1'b1);

    push = 1'b1;
    pop = 1'b1;
    din = 32'd8;
    #10;
    assert(full == 1'b1);
    assert(dout == 32'd1);

    for (i = 0; i < DEPTH; i++) begin
        push = 1'b0;
        pop = 1'b1;
        assert(dout == i + 1);
        assert(empty == 1'b0);
        #10;
    end

    assert(empty == 1'b1);

    #10 $finish;
end

endmodule
