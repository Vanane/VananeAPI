#pragma once
#include "tree.h"
#include <stdio.h>
#include <stdbool.h>


#define T_MULT "mult"
#define T_ADD "add"
#define T_MOD "mod"
#define T_DICE "dice"


void printFieldName(char * fieldName);
void printInt(char * fieldName, int value, bool isLastField);
void printString(char * fieldName, char * value, bool isLastField);
void printChar(char * fieldName, char value, bool isLastField);
void openObject();
void closeObject();
void printTreeAsJson(Node * tree, bool isLastObject);
void printMultAsJson(Node * mult);
void printAddAsJson(Node * add);
void printModAsJson(Node * mod);
void printDiceAsJson(Node * dice);
