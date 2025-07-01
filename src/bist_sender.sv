module bist_sender#(
    parameter int TEST_CHANNELS,
    parameter SEED,
    parameter int TEST_CASES
) (
    input  logic clk,
    input  logic reset,
    
    input  logic [TEST_CHANNELS-1:0] input_channels,

    output logic ready,
    output logic [TEST_CHANNELS-1:0] output_channels
);

logic [31:0] cases;
logic [31:0] rng_out;
logic [TEST_CHANNELS-1:0] test_output;
assign ready = cases == TEST_CASES;

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
        test_output <= '0;
    end else begin
        if (~ready) begin
            cases <= cases + 32'b1;
            test_output <= (test_output << 32) | rng_out;
        end
    end
end

always_comb begin
    if (ready)
        output_channels = input_channels;
    else
        output_channels = test_channels;
end

endmodule;
