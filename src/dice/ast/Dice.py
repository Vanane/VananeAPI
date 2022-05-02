from typing import Literal
from src.dice.ast.Modifier import Modifier

class Dice:
    left:int
    operator:Literal
    right:int
    modifier: Modifier


    def __init__(self, l, o, r, m) -> None:
        self.left = l
        self.operator = o
        self.right = r
        self.modifier = Modifier(m)