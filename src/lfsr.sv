module lfsr#(
    parameter SEED = 32'hdeadbeef
) (
    input  logic        clk,
    input  logic        reset,
    output logic [31:0] n
);

logic new_bit;
assign new_bit = n[7] ^ n[6] ^ n[2] ^ n[0];

always_ff @(posedge reset or posedge clk) begin
    if (reset) begin
        n <= SEED;
    end else begin
        n <= (n >> 1) | {new_bit, 31'b0};         
    end
end

endmodule
