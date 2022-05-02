from __future__ import absolute_import
from __future__ import print_function
import io
from bison import BisonParser
from six.moves import input


class DiceParser(BisonParser):
    # ----------------------------------------------------------------
    # lexer tokens - these must match those in your lex script (below)
    # ----------------------------------------------------------------
    tokens = ['NUMBER', 'MODOP', 'DICEOP', 'LPAREN', 'RPAREN', 'NEWLINE']

    # ------------------------------
    # precedences
    # ------------------------------
    precedences = (('left', ('d', 'D')),)
    # ---------------------------------------------------------------
    # These methods are the python handlers for the bison targets.
    # (which get called by the bison code each time the corresponding
    # parse target is unambiguously reached)
    #
    # WARNING - don't touch the method docstrings unless you know what
    # you are doing - they are in bison rule syntax, and are passed
    # verbatim to bison to build the parser engine library.
    # ---------------------------------------------------------------

    # Declare the start target here (by name)
    start = "S"

    def on_S(self, target, option, names, values):
        """
        S : expr NEWLINE
        """
        exit(0)

    def on_expr(self, target, option, names, values):
        """
        expr :	dice
            |	mult
            ;
        """
        # Code for managing an Expr
        return "expr"


    def on_dice(self, target, option, names, values):
        """
        dice :	NUMBER DICEOP NUMBER
            |	NUMBER DICEOP NUMBER MODOP NUMBER 
            ;
        """
        print("prout")
        # Code for managing a Dice
        return "dice"


    def on_mult(self, target, option, names, values):
        """
        mult :	NUMBER '(' expr ')'
            ;
        """
        # Code for managing a Mult
        return "mult"

    # -----------------------------------------
    # raw lex script, verbatim here
    # -----------------------------------------
    lexscript = r"""
    %{
    #include <stdio.h>
    #include <string.h>
    #define YYSTYPE void *
    #include "Python.h"
    #include "tmp.tab.h"
    yywrap() { return(1); }
    extern void *py_parser;
    extern void (*py_input)(PyObject *parser, char *buf, int *result, int max_size);
    #define returntoken(tok) yylval = PyUnicode_FromString(strdup(yytext)); return (tok);
    #define YY_INPUT(buf,result,max_size) { (*py_input)(py_parser, buf, &result, max_size); }
    %}

    %%
    [1-9][0-9]*     returntoken(NUMBER);
    [\-+]           returntoken(MODOP);
    [(]             returntoken(LPAREN);
    [)]             returntoken(RPAREN);
    [dD]            returntoken(DICEOP);
    
    .               { printf("unknown char %c", yytext[0]); }
    %%
    """

if __name__ == "__main__":
    p = DiceParser(debug=True, verbose=True)
    result = p.run(file='tmp.tmp', debug=False)
    print(result)
