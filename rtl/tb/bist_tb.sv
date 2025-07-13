module bist_tb;

parameter int TEST_CHANNELS = 70;
parameter SEED = 32'hdeadbeef;
parameter int TEST_CASES = 1000;

logic clk;
logic reset; 

logic [TEST_CHANNELS-1:0] sender_in;
logic sender_busy;
logic [TEST_CHANNELS-1:0] sender_out;

bist_sender#(
    .TEST_CHANNELS(TEST_CHANNELS),
    .SEED(SEED),
    .TEST_CASES(TEST_CASES)
) sender_uut (
    .clk(clk),
    .reset(reset),
    .input_channels(sender_in),
    .busy(sender_busy),
    .output_channels(sender_out)
);

logic [TEST_CHANNELS-1:0] receiver_in;
logic [TEST_CHANNELS-1:0] receiver_out;
logic receiver_busy, receiver_failed;

logic [TEST_CHANNELS-1:0] force_hi, force_lo;

assign receiver_in = ~force_lo & (force_hi | sender_out);

bist_receiver#(
    .TEST_CHANNELS(TEST_CHANNELS),
    .SEED(SEED),
    .TEST_CASES(TEST_CASES)
) receiver_uut (
    .clk(clk),
    .reset(reset),
    .input_channels(receiver_in),
    .busy(receiver_busy),
    .failed(receiver_failed),
    .output_channels(receiver_out)
);

always begin
    #5; clk = ~clk;
end

initial begin
    clk = 1'b0;
    sender_in = 70'hcafecafe;
    force_hi = '0;
    force_lo = '0;

    reset = 1'b0;
    #5;
    reset = 1'b1;
    #5;
    reset = 1'b0;

    while (receiver_busy)
        #5;

    assert(sender_in == receiver_out);

    reset = 1'b0;
    force_hi = 8'h80;
    force_lo = 8'h02;
    #5;
    reset = 1'b1;
    #5;
    reset = 1'b0;

    while (receiver_busy)
        #5;

    assert(receiver_failed);

    $finish;
end

endmodule
