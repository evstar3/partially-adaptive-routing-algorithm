module bist_sender_tb;

parameter int TEST_CHANNELS = 70;
parameter SEED = 32'hdeadbeef;
parameter int TEST_CASES = 1000;

logic clk;
logic reset; 
logic [TEST_CHANNELS-1:0] input_channels;
logic busy;
logic [TEST_CHANNELS-1:0] output_channels;

bist_sender#(
    .TEST_CHANNELS(TEST_CHANNELS),
    .SEED(SEED),
    .TEST_CASES(TEST_CASES)
) uut (
    .clk(clk),
    .reset(reset),
    .input_channels(input_channels),
    .busy(busy),
    .output_channels(output_channels)
);

always begin
    #5; clk = ~clk;
end

initial begin
    clk = 1'b0;
    reset = 1'b0;
    input_channels = 70'hcafecafe;

    #5;
    reset = 1'b1;
    #5;
    reset = 1'b0;

    while (busy)
        #5;

    assert(output_channels == input_channels);

    $finish;
end

endmodule
