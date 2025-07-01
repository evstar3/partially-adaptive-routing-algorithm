module bist_receiver#(
    parameter int TEST_CHANNELS = 70,
    parameter SEED = 32'hdeadbeef,
    parameter int TEST_CASES = 1000
) (
    input  logic clk,
    input  logic reset,
    
    input  logic [TEST_CHANNELS-1:0] input_channels,

    output logic ready,
    output logic failed,
    output logic [TEST_CHANNELS-1:0] output_channels
);

logic [31:0] cases;
logic [31:0] rng_out;
logic [TEST_CHANNELS-1:0] expected_input;
logic test_complete;
assign test_complete = cases == TEST_CASES;
assign ready = failed | test_complete;

lfsr#(
    .SEED(SEED)
) rng (
    .clk(clk),
    .reset(reset),
    .n(rng_out)
);

always_ff @(posedge clk or posedge reset) begin
    if (reset) begin
        cases <= '0;
        expected_input <= '0;
        failed <= '0;
    end else begin
        if (~ready) begin
            cases <= cases + 32'b1;
            expected_input <= (expected_input << 32) | rng_out;
            failed <= failed | (input_channels != expected_input);
        end
    end
end

always_comb begin
    if (ready & ~failed)
        output_channels = input_channels;
    else
        output_channels = 32'b0;
end

endmodule
