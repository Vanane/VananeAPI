%{
    #include <stdio.h>
    #include "y.tab.h"
%}

%%
[1-9][0-9]*     yylval.number=atoi(yytext);return NUMBER;
[\-+]           yylval.literal=yytext[0];return INTOP;
[dD]            yylval.literal=yytext[0];return DICEOP;
[\(\)]          return yytext[0];

[\n\r]          return NEWLINE;

.               return yytext[0];
%%
