module fifo_tb;

parameter int ADDR_WIDTH = 3;
parameter int DATA_WIDTH = 64;
parameter int DEPTH = 2 ** ADDR_WIDTH;

logic clk, reset;
logic push, pop;
logic empty, full;
logic [DATA_WIDTH-1] din, dout;

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

initial begin
    reset = 1'b1;
    #10;
    reset = 1'b0;

    assert(empty == 1'b1');
end

endmodule
