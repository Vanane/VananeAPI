#pragma once
#include <stdio.h>
#include <stdlib.h>


typedef struct TNode {
	int * value;
    int valueType; /* 0 = int, 1 = char, 2 = string */
	struct TNode * left;
	struct TNode * right;
	struct TNode * parent;
} Node;


void printPointerValue(int * pointer, int type);
Node * newTree();
Node * newNode(Node * left, int * value, Node * right, int valueType);
void printIndent(int indent);
void printTreeR(Node * tree, int indent);
void printTree(Node * tree);