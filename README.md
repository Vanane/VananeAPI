Launch server :
uvicorn main:app --reload

Compile parser :
lex dice.l && yacc -d dice.y && gcc lex.yy.c y.tab.c -o diceParser

## Installation

You will need :

-   Python 3.9.x
-   Bison
-   Flex
-   Yacc
-   Uvicorn
