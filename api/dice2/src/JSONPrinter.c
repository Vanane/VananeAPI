#include <stdio.h>
#include <stdbool.h>
#include "tree.h"

#define T_MULT "mult"
#define T_ADD "add"
#define T_MOD "mod"
#define T_DICE "dice"


void printFieldName(char * fieldName)
{
    printf("\"%s\":", fieldName);
}


void printInt(char * fieldName, int value, bool isLastField)
{
    printFieldName(fieldName);
    printf("%d", value);
    if(!isLastField)
        printf(", ");
}


void printString(char * fieldName, char * value, bool isLastField)
{
    printFieldName(fieldName);
    printf("\"%s\"", value);
    if(!isLastField)
        printf(", ");
}


void printChar(char * fieldName, char value, bool isLastField)
{
    printFieldName(fieldName);
    printf("\"%c\"", value);
    if(!isLastField)
        printf(",");
}


void openObject() { printf("{"); }
void closeObject() { printf("}"); }
void openArray() { printf("["); }
void closeArray() { printf("]"); }


void printTreeAsJson(Node * tree, bool isLastObject)
{
    if(tree != NULL)
    {
        switch((* tree).valueType)
        {
            case 0:
                // Do nothing
            break;
            case 1:
            break;
            case 2:
                if(!strcmp(T_MULT, (char *)tree->value)) { printMultAsJson(tree); }
                else
                if(!strcmp(T_ADD, (char *)tree->value))  { printAddAsJson(tree); }
                else
                if(!strcmp(T_MOD, (char *)tree->value))  { printModAsJson(tree); }
                else
                if(!strcmp(T_DICE, (char *)tree->value)) { printDiceAsJson(tree); }
            break;
        }
    }
    if(!isLastObject)
        printf(",");
}


void printMultAsJson(Node * mult)
{
    openObject();
    printString("type", (char *)mult->value, false);

    printInt("left", (* mult->left->value), false);

    printFieldName("right"); printTreeAsJson(mult->right, true);
    closeObject();
}


void printAddAsJson(Node * add)
{
    openObject();
    printString("type", (char *)add->value, false);

    printFieldName("left"); printTreeAsJson(add->left, false);

    printFieldName("right"); printTreeAsJson(add->right, true);
    closeObject();
}


void printModAsJson(Node * mod)
{
    openObject();

    printString("type", (char *)mod->value, false);    
    
    printFieldName("left"); printTreeAsJson((* mod).left, false);
    
    printInt("right", (* mod->right->value), true);
    closeObject();
}


void printDiceAsJson(Node * dice)
{
    openObject();
    printString("type", (char *)dice->value, false);

    printInt("left", (* dice->left->value), false);

    printInt("right", (* dice->right->value), true);

    closeObject();
}


void printError(char * message, bool isLastError)
{
    openObject();
    printString("type", "error", false);
    printString("value", message, true);
    closeObject();
    if(!isLastError)
        printf(",");
}

