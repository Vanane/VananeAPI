# Vanane API

## Installation

### Prerequisites

-   [Make](https://www.gnu.org/software/make/)
-   [GCC](https://www.gnu.org/software/gcc/)
-   [Python 3](https://www.python.org/download/releases/3.0/)
-   [Uvicorn](https://www.uvicorn.org/)
-   [A server](https://www.google.com/search?q=vps) (no way !)

### How to install

1. Clone the github repository into your machine
2. Compile the dice parser : `cd api/dice2/src` and `make`

### How to use

-   Launching the server : `uvicorn main:app --reload` (a `run` file at the root contains the command)

## Dice API

Dice API Uses Lex and Yacc to parse an expression from a dice language.

### Endpoints

#### /dice2/{expr}

##### Input

###### Dice language

_expr_ :

-   _dice_ :
    -   [0-9]+d[0-9]+
-   _mod_ :
    -   _dice_ +|- [0-9]+
-   _mult_ :
    -   [0-9]+(_expr_)

##### Outputs

###### Results

For a _dice_ or a _mod_ :

-   A JSON array of integers that contains each dice throw, with the last index being the total (only one element for a single dice throw)

For a _mult_ :

-   A JSON Array of arrays that contain the result of each serie of the inner expression

###### Errors

Syntax errors, expressions that exceed the limits.

Format :

-   A JSON array of JSON objects of following format :

```json
[
    {
        "type": "error",
        "value": "<string>"
    }
]
```

##### Limits

There are intended limits for the API, to avoid abuses of the API :

-   A dice can't have more than 100 throws
-   A dice nested in mults can't generate more than 1000 throws in total
-   The depth of a nested expression can't exceed 5

## TODO

-   Finish the docs of OpenAPI for Dice API

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
