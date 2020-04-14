grammar FileSyntax;

/*
    Parser Rules
*/

filesyntax : ((command | investigate) ';')* EOF;

investigate : (show | expect);

command : (insert | run);

expect: EXPECT_KWD ERROR_KWD INTEGER;

show : SHOW_KWD
     ( show_blocks
     | show_edges
     | show_initial_conditions
     | show_run
     );

show_blocks : BLOCK_KWD;
show_edges : EDGE_KWD;
show_initial_conditions : INITIAL_CONDITIONS_KWD;
show_run: RUN_KWD (show_run_all | show_run_selection);
show_run_all: ALL_KWD;
show_run_selection: node
                  | '(' node (',' node)* ')'
                  ;

insert : INSERT_KWD (insert_blocks | insert_edges | insert_initial_conditions) ;

insert_blocks : BLOCK_KWD create_block (',' create_block)* ;
create_block : create_state_block
             | create_not_gate
             | create_logic_gate_2_inputs
             | create_logic_gate_n_inputs
             ;
create_not_gate : NOT_KWD
                  block_name
                  input_pin_name
                  output_pin_name;

create_logic_gate_n_inputs : logic_gate_types_n
                             block_name
                             (input_pin_name (input_pin_name)*)
                             output_pin_name
                           ;
logic_gate_types_n : NOR_KWD
                   | AND_KWD
                   | XNOR_KWD
                   | XOR_KWD
                   | OR_KWD
                   | NAND_KWD
                   ;
create_logic_gate_2_inputs : logic_gate_types
                             block_name
                             input_pin_name
                             input_pin_name
                             output_pin_name
                           ;
logic_gate_types : AND2_KWD
                 | OR2_KWD
                 | NOR2_KWD
                 | NAND2_KWD
                 | XOR2_KWD
                 | XNOR2_KWD
                 ;


create_state_block : STATE_KWD pin_type block_name io_pin_name?;

pin_type : (INPUT_KWD | OUTPUT_KWD | INPUT_OUTPUT_KWD) ;

input_pin_name : NAME;
output_pin_name : NAME;
io_pin_name : NAME;

insert_edges : EDGE_KWD create_edge (',' create_edge)*;
create_edge : BETWEEN_KWD node AND_KWD one_or_multiple_nodes;
one_or_multiple_nodes : node
                      | '(' node (',' node)* ')'
                      ;

insert_initial_conditions : INITIAL_CONDITIONS_KWD initial_condition (',' initial_condition)*;
initial_condition : '(' condition (',' condition)* ')';
condition : node '=' node_value;

node : block_name '.' pin_name;
block_name : NAME;
pin_name : NAME;

node_value : INTEGER;

run : RUN_KWD;

/*
    Lexer Rules
*/

fragment LOWERCASE_LETTER : [a-z];
fragment UPPERCASE_LETTER : [A-Z];
fragment NUMBER : [0-9];
fragment LETTER : LOWERCASE_LETTER | UPPERCASE_LETTER;


OR_KWD : 'OR';
AND_KWD : 'AND';
NAND_KWD : 'NAND';
NOR_KWD : 'NOR';
XOR_KWD : 'XOR';
XNOR_KWD : 'XNOR';
NOT_KWD : 'NOT';

AND2_KWD : 'AND2';
OR2_KWD : 'OR2';
NOR2_KWD : 'NOR2';
NAND2_KWD : 'NAND2';
XOR2_KWD : 'XOR2';
XNOR2_KWD : 'XNOR2';

EXPECT_KWD: 'EXPECT';
ERROR_KWD: 'ERROR';
SHOW_KWD : 'SHOW';
ALL_KWD : 'ALL';
OUTPUT_KWD : 'OUT';
INPUT_KWD : 'IN';
INPUT_OUTPUT_KWD : 'INOUT';
STATE_KWD : 'STATE';
BLOCK_KWD : 'BLOCK' | 'BLOCKS';
EDGE_KWD : 'EDGE' | 'EDGES';
INITIAL_CONDITIONS_KWD : 'INITIAL CONDITION' | 'INITIAL CONDITIONS' | 'INIT COND';
INSERT_KWD : 'INSERT';
BETWEEN_KWD : 'BETWEEN' | 'BTWN';
RUN_KWD : 'RUN';

VERBOSE_PRM : '-' ('VERBOSE' | 'V');


INTEGER : NUMBER+;
NAME : (LETTER | NUMBER)+;

COMMENT : '/*' .*? '*/' -> skip ; // .*? matches anything until the first */
WHITESPACE : (SPACE | TAB) -> skip;
SPACE : ' ';
TAB : '\t';
NEWLINE : ('\r' | '\n' | '\r' '\n') -> skip;
UNKNOWN_CHAR : . ;
