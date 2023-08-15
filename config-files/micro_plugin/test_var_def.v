module xxx(
    input           signed            a_1                    , 
    input           signed            a_2                    , 
    input    reg    signed            a_3                    , 
    input           signed [dw:0]     a1_x                    , 
    input           signed [dw:0]     a2_x                    , 
    input    reg    signed [dw:0]     a3_x                    , 
    output   reg    signed [dw:0]     a1a                    , 
    output   reg    signed [dw:0]     a2a                    , 
    output   reg    signed [dw:0]     a3a                    , 
);

///{user-variable-define-begin
///}user-variable-define-end

///{auto-variable-define-begin
wire  [  8:0]              a_1                                     ;
wire  [  6:0]              b_1                                     ;
wire  [WIDTH_S -1:0]       a1_x                                    ;
reg   [  8:0]              a_2                                     ;
reg   [  6:0]              b_2                                     ;
reg   [WIDTH_S -1:0]       a2_x                                    ;
reg   [  8:0]              a_2                                     ;
reg   [  6:0]              b_2                                     ;
reg   [WIDTH_S -1:0]       a2_x                                    ;
///}auto-variable-define-end


assign a_1                 =   xxxx                ;//{uw9}
assign b_1                 =   xxxx                ;//{uw7}
assign a1_x                =   xxxx                ;//{uw<WIDTH_S>}

always 
    a_2                 =   xxxx                ;//{ur9}
    b_2                 =   xxxx                ;//{ur7}
    a2_x                =   xxxx                ;//{ur<WIDTH_S>}

    a_2                <=   xxxx                ;//{ur9}
    b_2                <=   xxxx                ;//{ur7}
    a2_x               <=   xxxx                ;//{ur<WIDTH_S>}
    





