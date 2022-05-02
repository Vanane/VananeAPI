%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <stdbool.h>
    #include "tree.c"
    #include "stack.c"
    
    extern FILE* yyin;
    
    Node * ASTroot;

    Stack * nodes;

    Node * curNode;

    int * throwDices(int amount, int value, int bonus);
    void detect(char * thing);
%}

%union {   
    int number;
    char literal;
    char * string;    
    struct TNode * node;
}

%start S

// %token NUMBER DICEOP INTOP

%token <number> NUMBER
%token DICEOP
%token <literal> INTOP
%token NEWLINE

%% /* beginning of rules section */

S       :   expr
            {
                ASTroot = (Node *) pop(nodes);
            }
        ;

expr    :   mult    /* Serie multiplier */
        |   dAdd    /* Dice addition */
        |   dMod
        |   dice
        ;

mult    :   NUMBER '(' expr ')'
            { 
                detect("multiplier");
                Node * l = newNode(NULL, &($1), NULL, 0);
                Node * r = pop(nodes);
                Node * ret = newNode(l, (int *)("mult"), r, 2);
                push(nodes, ret);
            }
        ;

dAdd    :   dOp INTOP dOp
            {
                Node * r = (Node *) pop(nodes);
                Node * l = (Node *) pop(nodes);

                Node * ret = newNode(l, (int *)("add"), r, 2);
                push(nodes, ret);
            }
        ;

dOp     :   '(' dMod ')'
        |   dice
        ;

dMod    :   dice INTOP NUMBER
            {
                Node * l = (Node *) pop(nodes);
                Node * r = newNode(NULL, &($3), NULL, 0);                
                Node * ret = newNode(l, (int *)("mod"), r, 2);
                push(nodes, ret);
            }
        ;

dice    :   NUMBER DICEOP NUMBER
            {
                detect("dice");
                Node * l = newNode(NULL, &($1), NULL, 0);
                Node * r = newNode(NULL, &($3), NULL, 0);
                printf("%d\n", $3);
                Node * ret = newNode(l, (int *)("dice"), r, 2);   
                push(nodes, ret);
            }
        ;
%%

int main(int argc, char** argv)
{
    if(argc > 1)
    {
        yyin = fmemopen(argv[1], strlen(argv[1]), "r");
        nodes = newStack(10, false);

        int result = yyparse();
        printf("result : %d\n", result);

        printTree(ASTroot);
    }
    else
    {
        return 1;
    }
}


void detect(char * thing)
{
    printf("Detected %s\n", thing);
    fflush(stdout);
}


int yyerror(s)
char *s;
{
	fprintf(stderr, "%s\n",s);
}

int yywrap()
{
	return(1);
}
