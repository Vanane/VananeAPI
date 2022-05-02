from copyreg import constructor
from curses.ascii import isblank
from typing import Literal

class Tokenizer:
    i:int
    sentence:str
    

    operators = ['+', '-']
    diceOperators = ['d', 'D']
    symbols = ['(', ')']


    # Constructor, takes the sentence/code to read
    def __init__(self, s):
        self.sentence = s


    # Starts reading the sentence and prints every token
    def tokenize(self):
        ret = []
        self.i = 0
        while(not self.endOfFile()):
            token = self.readToken()
            if(token != None and not self.isBlank(token)):
                ret.append(token)
        return ret


    # Increments the reader and returns the new char, or False if end of string
    def nextChar(self):
        try:
            self.i = self.i + 1
            return self.peekChar()
        except IndexError:
            return False


    # Returns True if index is out of bounds, or if the reader reads an empty literal, False otherwise
    def endOfFile(self):
        try:
            if(self.i >= len(self.sentence)): # If reader index is greater or equals the length of the input
                return True
            
            char = self.peekChar()
            return char == '' or char == None or char =='\0' or not char
        except IndexError: # if index is out of bounds, for some reason
            return True
        return False


    # Returns the current literal the reader it pointed to, or False if end of string
    def peekChar(self):
        if(self.i < len(self.sentence)):
            return self.sentence[self.i]
        else:
            return False


    # Reads the next token in the sentence, and determines the type of the token
    def readToken(self):
        nextChar = self.peekChar()
        print("DEBUG : char is '" + nextChar + "' (ascii : " + str(ord(nextChar)) + ")")
        # Try to read a number
        if(self.isNumber(nextChar)):
            print("DEBUG : reading number")
            return self.readNumber()

        if(self.isOperator(nextChar)):
            print("DEBUG : reading operator")
            return self.readOperator()

        if(self.isSymbol(nextChar)):
            print("DEBUG : reading other symbol")
            return self.readSymbol()

        if(self.isLetter(nextChar)):
            print("DEBUG : reading string or char")
            return self.readString()

        print("DEBUG : char either blank or invalid, or not supported, skipping")
        self.nextChar()
        return None


    # Reads the sentence while the given function or lambda is true, and returns the read token
    # Ex : readWhile(lambda x: x == '0') will read each literal until the current literal isn't 0 anymore
    def readWhile(self, cond):
        start = self.i
        end = self.i
        while(cond(self.peekChar()) and not self.endOfFile()):
            self.nextChar()
            end += 1        
        return self.sentence[start:end] # Substring in Python doesn't include the caracter at the index 'end'


    # Returns a token of type number
    def readNumber(self):
        return { 'type':'number', 'value': self.readWhile(self.isNumber) }


    # Returns a token of type string
    def readString(self):
        return { 'type':'string',  'value': self.readWhile(self.isLetter) }


    # Returns a token of type operator
    def readOperator(self):
        nextChar = self.peekChar()
        self.nextChar()
        return { 'type':'operator',  'value': nextChar }


    # Returns a token of type symbol
    def readSymbol(self):
        nextChar = self.peekChar()
        self.nextChar()
        return { 'type':'symbol',  'value': nextChar }


    # Returns True if literal is None, empty, space, new line or return, False otherwise
    def isBlank(self, expr:Literal):
        return expr == None or expr == '' or expr == '\n' or expr == ' ' or expr == '\r'


    # Returns True if literal is a known operator, False otherwise
    def isOperator(self, expr:Literal):
        return expr in self.operators or expr in self.diceOperators


    # Returns True if literal is a known symbol, False otherwise
    def isSymbol(self, expr:Literal):
        return expr in self.symbols


    # Returns True if literal can be converted to int, False otherwise
    def isNumber(self, expr:Literal):
        try: 
            int(expr)
            return True
        except ValueError:
            return False


    # Returns True if literal passes [a-zA-Z], False otherwise
    def isLetter(self, expr:Literal):
        try:
            if(self.isBlank(expr)):
                return False
            else:
                o = ord(expr)
                return ((o >= ord('A') and o <= ord('Z')) or (o >= ord('a') and o <= ord('z')))
        except TypeError:
            return False