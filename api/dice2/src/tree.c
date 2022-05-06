#include <stdio.h>
#include <stdlib.h>


typedef struct TNode {
	int * value;
    int valueType; /* 0 = int, 1 = char, 2 = string */
	struct TNode * left;
	struct TNode * right;
	struct TNode * parent;
} Node;


void printPointerValue(int * pointer, int type)
{
    if(pointer == NULL)
        printf("NULL");
    else
    {
        switch(type)
        {
            case 0:
                printf("%d", (* pointer));
            break;
            case 1:
                printf("%c", (* pointer));
            break;
            case 2:
                printf("%s", (char *)pointer);
            break;
            default:
            break;
        }
    }
}


Node * newTree()
{
    Node * root = malloc(sizeof(Node));
    (* root).left = NULL;
    (* root).value = NULL;
    (* root).right = NULL;
    (* root).valueType = 0;
    return root;
}


Node * newNode(Node * left, int * value, Node * right, int valueType)
{
    Node * node = malloc(sizeof(Node));
    (* node).left = left;
    (* node).value = value;
    (* node).right = right;
    (* node).valueType = valueType;
    return node;
}


void printIndent(int indent)
{
    for(int i = 1; i < indent; i++)
    {
        printf(" ");
    }
    printf("-");
    fflush(stdout);
}


void printTreeR(Node * tree, int indent)
{
    if(tree != NULL)
    {
        printTreeR((* tree).left, (indent + 4));

        printIndent(indent);
        printPointerValue((* tree).value, (* tree).valueType);
        printf("\n");

        printTreeR((* tree).right, (indent + 4));
    }
}


void printTree(Node * tree)
{
    if(tree != NULL)
    {
        printTreeR(tree, 1);
    }
}


/*
int main()
{
    int a = 1;
    int b = 2;
    int c = 5;
    int d = 18;
    int e = 987;


            Node * left2 = newNode(NULL, &a, NULL, 0);
                Node * left3 = newNode(NULL, &c, NULL, 0);
            Node * right2 = newNode(left3, &d, NULL, 0);
        Node * left1 = newNode(left2, &b, right2, 0);
        Node * right1 = newNode(NULL, &e, NULL, 0);
    Node * root = newTree();

    (*root).left = left1;
    (*root).right = right1;

    printTree(root);
}
*/
