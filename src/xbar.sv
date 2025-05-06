/*
module xbar2#(
    parameter int FLIT_SIZE = 32
) (
    input logic [FLIT_SIZE-1:0] din0,
    input logic [FLIT_SIZE-1:0] din1,

    input logic swap;

    output logic [FLIT_SIZE-1:0] dout0,
    output logic [FLIT_SIZE-1:0] dout1
);

always_comb begin
    if (swap) begin
        dout0 = din0;
        dout1 = din1;
    end else begin
        dout0 = din1;
        dout1 = din0;
    end
end

endmodule


module xbar3#(
    parameter int FLIT_SIZE = 32
) (
    input logic [FLIT_SIZE-1:0] din0,
    input logic [FLIT_SIZE-1:0] din1,
    input logic [FLIT_SIZE-1:0] din2,

    input logic [2:0] swap,

    output logic [FLIT_SIZE-1:0] dout0,
    output logic [FLIT_SIZE-1:0] dout1,
    output logic [FLIT_SIZE-1:0] dout2
)

logic [FLIT_SIZE-1:0] stage1 [2:0];

xbar2#(
    .FLIT_SIZE(FLIT_SIZE)
) xb0 (
    .din0(din0),
    .din1(din1),
    .swap(swap[0]),
    .dout0(stage1[0]),
    .dout1(stage1[1])
);

assign stage1[2] = din2;

logic [FLIT_SIZE-1:0] stage2 [2:0];

xbar2#(
    .FLIT_SIZE(FLIT_SIZE)
) xb0 (
    .din0(stage1[2]),
    .din1(stage1[3]),
    .swap(swap[1]),
    .dout0(stage2[2]),
    .dout1(stage1[3])
);

assign stage2[0] = stage1[0];

xbar2#(
    .FLIT_SIZE(FLIT_SIZE)
) xb0 (
    .din0(stage2[0]),
    .din1(stage2[1]),
    .swap(swap[2]),
    .dout0(dout0),
    .dout1(dout1)
);

assign dout2 = stage2[2];

endmodule

*/

module xbar#(
    parameter int INPUTS = 7,
    parameter int FLIT_SIZE = 32
) (
    input logic [FLIT_SIZE-1:0] din [INPUTS-1:0],
    input logic [INPUTS*$clog2(INPUTS)-INPUTS:0] swap,
    output logic [FLIT_SIZE-1:0] dout [INPUTS-1:0]
);

genvar curr_swap, i;
generate
    if (INPUTS == 2) begin
        if (swap[0]) begin
            assign dout[0] = din[1];
            assign dout[1] = din[0];
        end else
            assign dout = din;
    end else if (INPUTS == 3) begin
        logic [FLIT_WIDTH-1:0] stage1, stage2 [INPUTS-1:0];

        xbar#(
            .INPUTS(2),
            .FLIT_SIZE(FLIT_SIZE)
        ) xb0 (
            .din(din[1:0]),
            .swap(swap[0]),
            .dout(stage1[0:1])
        )
        assign stage1[2] = din[2];

        xbar#(
            .INPUTS(2),
            .FLIT_SIZE(FLIT_SIZE)
        ) xb0 (
            .din(stage1[2:1]),
            .swap(swap[1]),
            .dout(stage2[2:1])
        )
        assign stage2[0] = stage1[0];

        xbar#(
            .INPUTS(2),
            .FLIT_SIZE(FLIT_SIZE)
        ) xb0 (
            .din(stage2[1:0]),
            .swap(swap[0]),
            .dout(dout[1:0])
        )
        assign dout[2] = stage2[2];
    end else if (INPUTS % 2 == 0) begin
        logic [FLIT_WIDTH-1:0] stage1, stage2, stage3, stage4 [INPUTS-1:0];

        for (i = 0; i < INPUTS / 2; i++) begin
            xbar#(
                .INPUTS(2),
                .FLIT_SIZE(FLIT_SIZE)
            ) xbin (
                .din(din[2*i + 1:2*i]),
                .swap(swap[curr_swap]),
                .dout(stage1[2*i + 1:2*i])
            )
            curr_swap++;
        end

        for (i = 0; i < INPUTS / 2; i++) begin
            assign stage2[i] = stage1[2*i];
            assign stage2[INPUTS/2 + i] = stage1[2*i + 1];
        end

        for (i = 0; i < 2; i++) begin
            xbar#(
                .INPUTS(INPUTS / 2),
                .FLIT_SIZE(FLIT_SIZE)
            ) xbmid (
                .din(stage2[(INPUTS/2)*(i+1)-1:(INPUTS/2)*i),
                .swap(swap[curr_swap + INPUTS/2 - 1:curr_swap]),
                .din(stage3[(INPUTS/2)*(i+1)-1:(INPUTS/2)*i)
            )
            curr_swap += INPUTS / 2;
        end

        for (i = 0; i < INPUTS / 2; i++) begin
            assign stage4[2*i] = stage3[i];
            assign stage4[2*i + 1] = stage3[INPUTS/2 + i];
        end

        assign dout[1:0] = stage4[1:0];
        for (i = 1; i < INPUTS / 2; i++) begin
            xbar#(
                .INPUTS(2),
                .FLIT_SIZE(FLIT_SIZE)
            ) xbout (
                .din(stage4[2*i + 1:2*i]),
                .swap(swap[curr_swap]),
                .dout(dout[2*i + 1:2*i])
            )
            curr_swap++;
        end
    end
endgenerate

endmodule
