    input           signed                 aaa99       , 
    input           signed                 aaa_bb      , 
    input           signed                 aaa_99      , 
    input           signed [dw*a-1:0]      aaa         , 
    output   reg    signed [99:0]          aaa         , 
    output   wire   signed [(a*b-1):0]     aaa         , 
    output   reg           [a*b-1:0]       aaa         , 
    output   wire          [dw:0]          aaa         , 

 reg    signed [dw:0]         saaa                ; 
 wire   signed [dw:0]         aaa                 ; 
 wire   signed [dw:0]         aaa [xxx*a-1:0]     ; 
 wire   signed [dw*a-1:0]     aaa [xxx*a-1:0]     ; 
 wire   signed [dw*a-1:0]     aaa [99:0]          ; 
 reg           [dw:0]         aaa                 ; 
 wire          [dw:0]         aaa                 ; 



 // ./test_inst.v
TEST_INST  U_TEST_INST(
    .a    (a     ), //I_p
    .b    (b     ), //I_p
    .c    (c     ), //I_p
    .d    (d     ), //I_p
    .e    (e     ), //I_p
    .f    (f     ), //O_p
    .g    (g     ), //O_p
    .h    (h     )  //O_p
);


 // ./test_inst_para.v
TEST_INST  #(
    .dw     (INST_PARA      ), 
    .dwa    (INST_PARA      ), 
    .dwb    (INST_PARA      ), 
    .dwc    (INST_PARA)     )  
U_TEST_INST(
    .a    (a     ), //I_p
    .b    (b     ), //I_p
    .c    (c     ), //I_p
    .d    (d     ), //I_p
    .e    (e     ), //I_p
    .f    (f     ), //O_p
    .g    (g     ), //O_p
    .h    (h     )  //O_p
);


///* test inst align
TEST_INST  U_TEST_INST(
    .a          (a [(a*b_+c)-1:0 ]             ), //I_p
    .b          (b [sss-1:0]                   ), //I_p
    .c          (c [ABC-1:0]                   ), //I_p
    .c          (c [ABC-1    :0  ]             ), //I_p
    .d          (d [99:0]                      ), //I_p
    .e          (e                             ), //I_p
    .f          (f                             ), //O_p
    .g          ({adfa,fsa}                    ), //O_p
    .g          ({adfa,   fsa}                 ), //O_p
    .g          (adfa [a:0],   fsa[b-1:0]      ), //O_p
    .g          (adfa [a-1:0],   fsa[b-1:0]    ), //O_p
    .g          (adfa [111:0],   fsa[b-1:0]    ), //O_p
    .g_xxx      (adfa [111:0],   fsa[b-1:0]    ), //O_p
    .g_x_99x    (adfa [111:0],   fsa[b-1:0]    ), //O_p
    .h          (h                             )  //O_p
);


    assign a                     =   b                                       ;
    assign a                     =   c                         [xx:0]        ;
    assign a                     =   d                         [999:0]       ;
    assign a_999[10:    0]       =   f                                       ;
    assign a99  [19:0]           =   c                         [xx:   0]     ;
    assign a    [xxx:0]          =   d                         [999:0   ]    ;
    assign a    [yyy:0]          =   c                         [xx:0]        ;
    assign a    [yyy:0]          =   c                         [xx+yyy-1:0]  ;
    assign a    [yy+xx:0]        =   c                         [xx+yyy-1:0]  ;
    assign a    [yy+xx-1:0]      =   c                         [xx+yyy-1:0]  ;
    assign a    [(yy*a+xx)-1:0]  =   c                         [xx+yyy-1:0]  ;
    assign a    [(yy*a+xx)-1:0]  =   {a,b,v}                                 ;
    assign a    [(yy*a+xx)-1:0]  =   {a,  b, v}                              ;
    assign a    [(yy*a+xx)-1:0]  =   {a[xxx:0],  b[99:0], v[0]}              ;

    assign {a,b,c}                     =   {a[xxx:0],  b[99:0], v[0]}  ;
    assign {a[xxx:0],  b[99:0], v[0]}  =   {a[xxx:0],  b[99:0], v[0]}  ;

///always
    a                 =   b                       ;
    a                 =   c         [xx:0]        ;
    a                 =   d         [999:0]       ;
    a[10:       0  ]  =   f                       ;
    a[19:0]           =   c         [xx:0]        ;
    a[xxx:0]          =   d         [999:0]       ;
    a[yyy:0]          =   c         [xx:0]        ;
    a[yyy:0]          =   c         [xx+yyy-1:0]  ;
    a[yy+xx:0]        =   c         [xx+yyy-1:0]  ;
    a[yy+xx-1:0]      =   c         [xx+yyy-1:0]  ;
    a[(yy*a+xx)-1:0]  =   c         [xx+yyy-1:0]  ;
    a[(yy*a+xx)-1:0]  =   c         [xx+yyy-1:0]  ;
    a[(yy*a+xx)-1:0]  =   {a,b,v}                 ;
    a[(yy*a+xx)-1:0]  =   {a,  b, v}              ;

    a                         [(yy*a+xx)-1:0]  =   {a[xxx:0],  b[99:0], v[0]}  ;
    {a,b,c}                                    =   {a[xxx:0],  b[99:0], v[0]}  ;
    {a[xxx:0],  b[99:0], v[0]}                 =   {a[xxx:0],  b[99:0], v[0]}  ;
///<=
    a                 <=  b              ;
    a                 <=  c[xx:0]        ;
    a                 <=  d[999    :0]   ;
    a[10:0]           <=  f              ;
    a[19:0]           <=  c[xx:0]        ;
    a[xxx:0]          <=  d[999:0]       ;
    a[yyy:0]          <=  c[xx:0]        ;
    a[yyy:0]          <=  c[xx+yyy:0]    ;
    a[yyy:0]          <=  c[xx+yyy-1:0]  ;
    a[yyy:0]          <=  c[xx+yyy-1:0]  ;
    a[yy+xx:0]        <=  c[xx+yyy-1:0]  ;
    a[yy+xx-1:0]      <=  c[xx+yyy-1:0]  ;
    a[(yy*a+xx)-1:0]  <=  c[xx+yyy-1:0]  ;
    a[(yy*a+xx)-1:0]  <=  c[xx+yyy-1:0]  ;
    a[(yy*a+xx)-1:0]  <=  c[xx+yyy-1:0]  ;

    a[(yy*a+xx)-1:0]  <=  {a,b,v}                     ;
    a[(yy*a+xx)-1:0]  <=  {a,  b, v}                  ;
    a[(yy*a+xx)-1:0]  <=  {a[xxx:0],  b[99:0], v[0]}  ;

    {a,b,c}                     <=  {a[xxx:0],  b[99:0], v[0]}  ;
    {a[xxx:0],  b[99:0], v[0]}  <=  {a[xxx:0],  b[99:0], v[0]}  ;

wavedrom:
\\                                             _________         _
\\SN:teatsa                        SW:________/         \_______/    SD:00001111100001
\\                                             _________         _
\\SN:tea                           SW:________/         \_______/    SD:00001111100001
