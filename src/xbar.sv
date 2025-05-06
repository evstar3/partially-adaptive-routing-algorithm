module xbar#(
    parameter int INPUTS = 7,
    parameter int FLIT_SIZE = 32
) (
    input logic [INPUTS-1:0] [FLIT_SIZE-1:0] din,
    input logic [INPUTS-1:0] [$clog2(INPUTS)-1:0] dest,

    output logic [INPUTS-1:0] [FLIT_SIZE-1:0] dout 
);

logic [INPUTS-1:0] [INPUTS-1:0] [FLIT_SIZE-1:0] temp;

genvar source_var, dest_var;
generate
    for (source_var = 0; source_var < INPUTS; source_var++)
        for (dest_var = 0; dest_var < INPUTS; dest_var++)
            always_comb
                temp[dest_var][source_var] = {32{dest[source_var] == dest_var}} & din[source_var];
endgenerate

genvar dout_var;
generate
    for (dout_var = 0; dout_var < INPUTS; dout_var++) begin
        logic [FLIT_SIZE-1:0] or_of_array;
        int j;
        always_comb begin
            or_of_array = 0;
            foreach(temp[dout_var][j])
                or_of_array |= temp[dout_var][j];
        end
        assign dout[dout_var] = or_of_array;
    end
endgenerate

endmodule
