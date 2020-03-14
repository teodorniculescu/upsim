grammar FileSyntax;

/*
    Parser Rules
*/

filesyntax : (insert)* EOF;

insert : INSERT_KWD (insert_blocks | insert_edges | insert_initial_conditions) ';';

insert_blocks : BLOCK_KWD create_block (',' create_block)* ;
create_block : create_state_block | create_and2_block;

create_and2_block : AND2_KWD block_name input_pin_name input_pin_name output_pin_name;
create_state_block : STATE_KWD block_name io_pin_name;

block_name : NAME;
input_pin_name : NAME;
output_pin_name : NAME;
io_pin_name : NAME;

insert_edges : EDGE_KWD create_edge (',' create_edge)*;
create_edge : BETWEEN_KWD node AND_KWD node;
node : NAME '.' NAME;

insert_initial_conditions : INITIAL_CONDITIONS_KWD initial_condition (',' initial_condition)+;
initial_condition : '(' condition (',' condition)* ')';
condition : NAME '.' NAME '=' INTEGER;

/*
    Lexer Rules
*/

fragment LOWERCASE_LETTER : [a-z];
fragment UPPERCASE_LETTER : [A-Z];
fragment NUMBER : [0-9];
fragment LETTER : LOWERCASE_LETTER | UPPERCASE_LETTER;

OUTPUT_KWD : 'OUT';
INPUT_KWD : 'IN';
INPUT_OUTPUT_KWD : 'INOUT';
STATE_KWD : 'STATE';
BLOCK_KWD : 'BLOCK' | 'BLOCKS';
EDGE_KWD : 'EDGE' | 'EDGES';
INITIAL_CONDITIONS_KWD : 'INITIAL CONDITION' | 'INITIAL CONDITIONS';
INSERT_KWD : 'INSERT';
AND2_KWD : 'AND2';
BETWEEN_KWD : 'BETWEEN';
AND_KWD : 'AND';

PIN_TYPE : INPUT_KWD | OUTPUT_KWD | INPUT_OUTPUT_KWD;
INTEGER : NUMBER+;
NAME : (LETTER | NUMBER)+;

COMMENT : '/*' .*? '*/' -> skip ; // .*? matches anything until the first */
WHITESPACE : (' ' | '\t') -> skip;
NEWLINE : ('\r' | '\n' | '\r' '\n') -> skip;
ANY : . ;
