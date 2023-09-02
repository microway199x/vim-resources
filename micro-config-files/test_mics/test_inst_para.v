
module TEST_INST#(
    parameter dw      = 10             , 
    parameter dwa     = 11             , 
    parameter dwb     = x              , 
    parameter dwc     = dw + dwa       , ///
    parameter dwc     = dw + dwa       , /// 
    parameter dwc     = (dw + dwa)     , /// 
    parameter dwc     = (dw + dwa)       /// 
)(
    input                               a      , 
    input                  [22:0]       b      , 
    input           signed [22:0]       c      , 
    input           signed [dw:0]       d      , 
    input           signed [dw+1:0]     e      , 

    output   reg    signed [22:0]       f      , 
    output   wire   signed [dw:0]       g      , 
    output          signed [dw+1:0]     h        

);
