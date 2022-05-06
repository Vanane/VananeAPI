%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <stdbool.h>
    #include <stdarg.h>
    
    #include "stack.h"
    #include "tree.h"
    #include "JSONPrinter.h"
    
    /* YACC reserved variable for input arguments */
    extern FILE* yyin;
    extern FILE* yyabortlab;
    
    /* Output tree */
    Node * ASTroot;

    /* Stack used to store the nodes when YACC parses each syntax.
    Alternative to using $$ which recycles pointers, and therefore makes it difficult to build an  AST. */
    Stack * nodes;

    /* Stack used to store potential errors, and pop and prints them when the parsed finishes. */
    Stack * errors;

    /* Some constants to define the limits of the system. If the given expression exceeds those limits, errors are thrown and the API call is aborted */
    const int MAXIMUM_DICE_COUNT = 100;
    const int MAXIMUM_THROWS = 1000;
    const int MAXIMUM_NESTS = 5;

    int throwCountSentinel = 0;
    int nestCountSentinel = 0;

    /* Additional functions */

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
                throwCountSentinel *= $1;
                nestCountSentinel += 1;

                if(throwCountSentinel > MAXIMUM_THROWS)
                {
                    char err[256];
                    snprintf(err, 256, "Value error : nested dice count limit exceeded (%d > %d)", throwCountSentinel, MAXIMUM_THROWS);
                    yyerror(err);
                    YYABORT;
                }

                else if(nestCountSentinel > MAXIMUM_NESTS)
                {
                    char err[256];
                    snprintf(err, 256, "Value error : nested command limit exceeded (%d > %d)", nestCountSentinel, MAXIMUM_NESTS);
                    yyerror(err);
                    YYABORT;
                }
                else 
                {
                    int * S1 = malloc(sizeof(int));

                    memcpy(S1, &($1), sizeof(int));

                    Node * l = newNode(NULL, S1, NULL, 0);
                    Node * r = pop(nodes);
                    Node * ret = newNode(l, (int *)(T_MULT), r, 2);
                    push(nodes, ret);
                }
            }
        ;

dAdd    :   dOp INTOP dOp
            {
                Node * r = (Node *) pop(nodes);
                Node * l = (Node *) pop(nodes);
                Node * ret = newNode(l, (int *)(T_ADD), r, 2);
                push(nodes, ret);
            }
        ;

dOp     :   '(' dMod ')'
        |   dice
        ;

dMod    :   dice INTOP NUMBER
            {            
                int * S3 = malloc(sizeof(int));
            
                memcpy(S3, &($3), sizeof(int));
            
                Node * l = (Node *) pop(nodes);

                if($2 == '-')
                (* S3) *= -1;
                Node * r = newNode(NULL, S3, NULL, 0);


                Node * ret = newNode(l, (int *)(T_MOD), r, 2);
                push(nodes, ret);
            }
        ;

dice    :   NUMBER DICEOP NUMBER
            {
                throwCountSentinel += $1;
                if(throwCountSentinel > MAXIMUM_THROWS)
                {
                    char err[256];
                    snprintf(err, 256, "Value error : nested dice count limit exceeded (%d > %d)", throwCountSentinel, MAXIMUM_THROWS);
                    yyerror(err);
                    YYABORT;
                }                
                else if($1 > MAXIMUM_DICE_COUNT)
                {
                    char err[256];
                    snprintf(err, 256, "Value error : dice count limit exceeded (%d > %d)", $1, MAXIMUM_DICE_COUNT);
                    yyerror(err);
                    YYABORT;
                }
                else
                {
                    int * S1 = malloc(sizeof(int));
                    int * S3 = malloc(sizeof(int));

                    memcpy(S1, &($1), sizeof(int));
                    memcpy(S3, &($3), sizeof(int));

                    Node * l = newNode(NULL, S1, NULL, 0);
                    Node * r = newNode(NULL, S3, NULL, 0);

                    Node * ret = newNode(l, (int *)(T_DICE), r, 2);   
                    push(nodes, ret);
                }
            }
        ;
%%

int main(int argc, char** argv)
{
    if(argc > 1)
    {        
        yyin = fmemopen(argv[1], strlen(argv[1]), "r");
        nodes = newStack(10, false);
        errors = newStack(10, false);
        
        int error = yyparse();
        if(!error)
        {
            if(ASTroot == NULL)
            { 
                openObject();
                closeObject();
            }
            else
            {
                printTreeAsJson(ASTroot, true);
            }
            fflush(stdout);
        }
        else
        {
            openArray();
            while(peek(errors) != NULL)
            {
                bool last = false;
                int * elem = pop(errors);
                if(peek(errors) == NULL)
                    last = true;
                printError((char *) elem, last);
            }
            closeArray();
        }
        free(errors);
        free(nodes);
        free(ASTroot);
    }
    else
    {
        openObject();
        closeObject();
    }
}


int yyerror(s)
char *s;
{
    //fprintf(stderr, "%s", s);
    push(errors, s);
}


int yywrap()
{
	return(1);
}


