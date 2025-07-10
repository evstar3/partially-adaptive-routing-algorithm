module lfsr8#(
    parameter SEED = 8'hED
) (
    input  logic       clk,
    input  logic       reset,
    output logic [7:0] n
);

logic new_bit;
assign new_bit = n[4] ^ n[3] ^ n[2] ^ n[0];

always_ff @(posedge reset or posedge clk) begin
    if (reset) begin
        n <= SEED;
    end else begin
        n <= (n >> 1) | {new_bit, 7'b0};         
    end
end

endmodule
