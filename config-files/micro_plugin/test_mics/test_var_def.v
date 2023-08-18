module xxx(
    input                  [  8:0]               a_4       , 
    input                  [WIDTH_S -1:0]        a4_x      , 
    output   reg           [  6:0]               b_3       , 
    output   reg           [WIDTH_S :0]          b3_x      , 
    output   reg           [  6:0]               b_3       , 
    output   reg           [WIDTH_S*aa -1:0]     b3_x      , 
    output   reg           [WIDTH_S -1:0]        b3_x      , 
///{auto-port-define-begin
input        [  8:0]              a_5                                      ,
input        [WIDTH_S -1:0]       a5_x                                     ,
input        [  8:0]              a_7                                      ,
input        [WIDTH_S -1:0]       a7_x                                     ,
input        [  8:0]              a_8                                      ,
input        [WIDTH_S -1:0]       a8_x                                     ,
output       [  6:0]              b_1                                      ,
output wire  [WIDTH_S -1:0]       b1_x                                     ,
output reg   [  6:0]              b_2                                      ,
output reg   [WIDTH_S -1:0]       b2_x                                     ,
output       [  8:0]              b_6                                      ,
output       [WIDTH_S -1:0]       b6_x                                     ,
///}auto-port-define-end
);

///{user-variable-define-begin
 wire          [  8:0]            a_1              ; 
 wire          [WIDTH_S -1:0]     a1_x             ; 
 reg           [WIDTH_S -1:0]     a2_x [xxx:0]     ; 
 reg           [  8:0]            a_3 [999:0]      ; 
 reg           [WIDTH_S -1:0]     a3_x             ; 
///}user-variable-define-end

///{auto-variable-define-begin
wire  [WIDTH_S -1:0]       b21_x                                    ;
wire  [  8:0]              b31_x                                    ;
wire  [  9:0]              b41_x                                    ;
reg   [  8:0]              a_2                                      ;
reg   [  8:0]              a_21                                     ;
reg   [WIDTH_S -1:0]       a21_x                                    ;
reg   [WIDTH_S -1:0]       b31_x                                    ;
wire  [  8:0]              a_6                                      ;
wire  [WIDTH_S -1:0]       a6_x                                     ;
///}auto-variable-define-end


    assign a_1               =   xxxx  ;//{uw9}
    assign a1_x              =   xxxx  ;//{uw<WIDTH_S>}
    assign b_1               =   xxxx  ;//{uwo7}
    assign b1_x              =   xxxx  ;//{uwo<WIDTH_S>}
    assign b21_x[WID*A-1:0]  =   xxxx  ;//{uw<WIDTH_S>}
    assign b31_x[9-1:0]      =   xxxx  ;//{uw9}
    assign b41_x[9:0]        =   xxxx  ;//{uw10}

always 
    a_2               =   xxxx  ;//{ur9}
    a_21 [8:0]        =   xxxx  ;//{ur9}
    a2_x              =   xxxx  ;//{ur<WIDTH_S>}
    a21_x[WID*A-1:0]  =   xxxx  ;//{ur<WIDTH_S>}
    b_2               =   xxxx  ;//{uro7}
    b2_x              =   xxxx  ;//{uro<WIDTH_S>}

    a_3               <=  xxxx  ;//{ur9}
    a3_x              <=  xxxx  ;//{ur<WIDTH_S>}
    b_3  [a*b]        <=  xxxx  ;//{uro7}
    b3_x              <=  xxxx  ;//{uro<WIDTH_S>}
    b31_x[WID*A-1:0]  <=  xxxx  ;//{ur<WIDTH_S>}
    
///inst   
    .xxxxx    (a_4               ), //{uwi9}
    .xxxxx    (a4_x              ), //{uwi<WIDTH_S>}
    .xxxxx    (a_5               ), //{uwi9}
    .xxxxx    (a5_x              ), //{uwi<WIDTH_S>}
    .xxxxx    (a_6               ), //{uw9}
    .xxxxx    (a6_x              ), //{uw<WIDTH_S>}
    .xxxxx    (b_6               ), //{uwo9}
    .xxxxx    (b6_x              ), //{uwo<WIDTH_S>}
    .xxxxx    (a_7 [8:0]         ), //{uwi9}
    .xxxxx    (a7_x [WID-1:0]    ), //{uwi<WIDTH_S>}
    .xxxxx    (a_8      [8:0]         ), //{uwi9}
    .xxxxx    (a8_x        [WID-1:0]  ), //{uwi<WIDTH_S>}
///}auto-port-define-end





