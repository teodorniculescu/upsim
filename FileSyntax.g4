grammar FileSyntax;

/*
    Parser Rules
*/

filesyntax : (insert)* EOF;

insert : INSERT_KWD (insert_blocks | insert_edges | insert_initial_conditions) ';';

insert_blocks : BLOCK_KWD block (',' block)* ;
block : state_block | and2_block;

and2_block : AND2_KWD NAME NAME NAME NAME;
state_block : STATE_KWD NAME NAME;

insert_edges : EDGE_KWD edge (',' edge)*;
edge : BETWEEN_KWD node AND_KWD node;
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
