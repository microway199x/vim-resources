    input           signed            aaa        , 
    input           signed [dw:0]     aaa        , 
    output   reg    signed [dw:0]     aaa        , 
    output   wire   signed [dw:0]     aaa        , 
    output   reg           [dw:0]     aaa        , 
    output   wire          [dw:0]     aaa        , 

 reg    signed [dw:0]     saaa       ; 
 wire   signed [dw:0]     aaa        ; 
 reg           [dw:0]     aaa        ; 
 wire          [dw:0]     aaa        ; 



 // ./test_inst.v
TEST_INST  U_TEST_INST(
    .a         (a         ),//I_p
    .b         (b         ),//I_p
    .c         (c         ),//I_p
    .d         (d         ),//I_p
    .e         (e         ),//I_p
    .f         (f         ),//O_p
    .g         (g         ),//O_p
    .h         (h         ) //O_p
);


 // ./test_inst_para.v
TEST_INST  #(
    .dw        (INST_PARA),
    .dwa       (INST_PARA),
    .dwb       (INST_PARA),
    .dwc       (INST_PARA))
U_TEST_INST(
    .a         (a         ),//I_p
    .b         (b         ),//I_p
    .c         (c         ),//I_p
    .d         (d         ),//I_p
    .e         (e         ),//I_p
    .f         (f         ),//O_p
    .g         (g         ),//O_p
    .h         (h         ) //O_p
);
