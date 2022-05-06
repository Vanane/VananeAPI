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


Stack * newStack(int capacity, bool verbose)
{
    Stack * stack = malloc(sizeof(Stack));
    (* stack).capacity = capacity;
    (* stack).size = 0;
    (* stack).top = NULL;
    (* stack).verbose = verbose;
    return stack;
}


void push(Stack * stack, void * object)
{
    if((* stack).capacity > (* stack).size)
    {
        StackElem * elem = malloc(sizeof(StackElem));
        (* elem).value = object;
        (* elem).previous = (* stack).top;
        (* stack).top = elem;
        (* stack).size++;
    }
    else
    {
        if((* stack).verbose)
            printf("Stack capacity of %d exceeded !\n", (* stack).capacity);
    }
}


bool empty(Stack * stack)
{
    return (* stack).top == NULL;
}


int * pop(Stack * stack)
{
    if(!empty(stack))
    {
        StackElem * topElem = (* stack).top;
        (* stack).top = ((StackElem *)(* topElem).previous);
        return (* topElem).value;
    }
    else
    {
        if((* stack).verbose)
            printf("Stack is empty !\n");
        return NULL;
    }
}

int * peek(Stack * stack)
{       
    if(!empty(stack))
    {
        return (* (* stack).top).value;
    }
    else
    {
        if((* stack).verbose)
            printf("Stack is empty !\n");
        return NULL;
    }
}