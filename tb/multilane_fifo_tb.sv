module multilane_fifo_tb;

parameter int LANES = 2;
parameter int DEPTH_BITS = 2;
parameter int DATA_WIDTH = 32;
parameter int LANE_BITS = $clog2(LANES);
parameter int DEPTH = 2 ** DEPTH_BITS;

logic clk, reset;
logic [LANE_BITS-1:0] push_lane, pop_lane;
logic push, pop;
logic [LANES-1:0] empty, full;
logic [DATA_WIDTH-1:0] din, dout;

multilane_fifo #(
    .LANES(LANES),
    .DEPTH_BITS(DEPTH_BITS),
    .DATA_WIDTH(DATA_WIDTH)
) dut (
    .clk(clk),
    .reset(reset),
    .push_lane(push_lane),
    .push(push),
    .pop_lane(pop_lane),
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

int i, l;
initial begin
    reset = 1'b1;
    #10;
    reset = 1'b0;

    assert(&empty);

    push = 1'b1;
    pop = 1'b0;
    push_lane = '0;
    pop_lane = '0;
    for (i = 0; i < LANES * DEPTH; i++) begin
        din = i + 1;
        assert(~&full);
        #10;
        assert(~&empty);
        push_lane++;
    end

    assert(&full);
    assert(~|empty);

    push = 1'b0;
    pop = 1'b1;
    for (l = 0; l < LANES; l++) begin
        pop_lane = l;
        for (i = 0; i < DEPTH; i++) begin
            $display(pop_lane, dout);
            #10;
        end
        assert(empty[l]);
    end
    
    #10 $finish;
end

endmodule
