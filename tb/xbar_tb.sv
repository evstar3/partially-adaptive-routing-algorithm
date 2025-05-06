module xbar_tb;

parameter int INPUTS = 7;
parameter int FLIT_SIZE = 32;

logic [INPUTS-1:0] [FLIT_SIZE-1:0] din;
logic [INPUTS-1:0] [$clog2(INPUTS)-1:0] dest;
logic [INPUTS-1:0] [FLIT_SIZE-1:0] dout;

xbar#(
    .INPUTS(INPUTS),
    .FLIT_SIZE(FLIT_SIZE)
) dut (
    .din(din),
    .dest(dest),
    .dout(dout)
);

int i;
initial begin
    for (i = 0; i < INPUTS; i++)
        din[i] = 1 << i;

    for (i = 0; i < INPUTS; i++)
        //dest[i] = INPUTS - i - 1;
        dest[i] = 0;

    #5;

    $display("%x", din);
    $display("%b", dest);
    $display("%x", dout);

    #10 $finish;
end

endmodule
