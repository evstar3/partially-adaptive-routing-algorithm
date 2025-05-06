parameter int TYPE_FIELD_SIZE = 2;
parameter int HEADER_SIZE = TYPE_FIELD_SIZE;

parameter int BODY_SIZE = 30;
parameter int FLIT_SIZE = HEADER_SIZE + BODY_SIZE;

typedef enum logic [1:0] {
    BODY = 2'b00,
    HEAD = 2'b01,
    TAIL = 2'b11,
    INVALID = 2'b10
} flit_t;


