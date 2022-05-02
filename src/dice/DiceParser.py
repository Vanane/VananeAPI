from src.dice.ast.Expression import Expression


class DiceParser:
    tokens:list
    tree:Expression
    pointer:int


    def __init__(self, t:list):
        self.tokens = t
        self.pointer = 0


    def parse(self):
        try:
            self.tree = Expression(self)
            return self.tree
        except Exception as e:
            return str(e)


    def nextToken(self):
        self.pointer = self.pointer + 1
        return self.peekToken()


    def peekToken(self, offset = 0):
        if(self.pointer + offset < len(self.tokens)):
            return self.tokens[self.pointer + offset]
        return None


    def size(self):
        return len(self.tokens)
