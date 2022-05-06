#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct TStackElem {
    void * value;
    struct TStackElem *  previous;
} StackElem;


typedef struct TStack {
    int capacity;
    int size;
    int verbose;
    StackElem * top;
} Stack;


Stack * newStack(int capacity, bool verbose);
void push(Stack * stack, void * object);
bool empty(Stack * stack);
int * pop(Stack * stack);
int * peek(Stack * stack);