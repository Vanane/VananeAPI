import random
import re
import os
from .item import Item

# Constants
DEFAULT_FORMAT_FILE = "format"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class ItemGenerator:    
    words:dict
    relPath:str
    formatFile:str

    currentItem:Item


    def __init__(self, relPath:str, formats:str) -> None:
        if relPath is None:
            self.relPath = "./"
        else:
            self.relPath = relPath
        
        if formats is None:
            self.formatFile = DEFAULT_FORMAT_FILE
        else:
            self.formatFile = formats            
        self.words = dict()
        pass


    def getRandomElementInFile(self, file:str) -> str:
        fileContents:str
            
        if not file in self.words:
            # Caching the opened file
            fileContents = list(map( lambda el : el.split(';'), open(self.relPath + "/" + file + ".csv", "r").read().split('\n')))

            self.words[file] = fileContents
        else:
            fileContents = self.words[file]
        return fileContents[random.randint(0, len(fileContents) - 1)]

    # Returns a random int between min and max.
    # Parses tokens of the form :
    # {%randint <min:int> <max:int>%}
    # Ex : {%randint 0 10%} will generate a random number between 0 and 10
    def parseRandInt(self, token:list) -> str:
        try:
            return str(random.randint(int(token[1]), int(token[2])))
        except Exception as e:
            print("ERROR : " + str(e))
            return "error"


    # Returns a string of letters between 1 and 26 for lowercase, or 27 and 52 for uppercase
    # Parses tokens of the form :
    # {%randstr <min:int> <max:int> <len:int>%}
    # Ex : {%randstr 1 26 3%} will generate a random string of length 3 of lowercase characters
    def parseRandStr(self, token:list) -> str:
        try:
            return ''.join(random.choice(ALPHABET[int(token[1]) - 1:int(token[2])]) for i in range(int(token[3])))
        except Exception as e:
            print("ERROR : " + str(e))
            print(token)
            return "error"


    # Returns a string chosen randomly between the given possibilities
    #Parses tokens of the form :
    # {%choose <elem1> <elem2> ...%}
    # Ex : {%choose a bb ccc dddd%} will choose one of the 4 possibilities
    def parseChoose(self, token:list) -> str:
        try:
            return token[random.choice(range(1, len(token) + 1))]
        except Exception as e:
            print("ERROR : " + str(e))
            print(token)
            return "error"
            

    # An expression is a calculated token instead of a line randomly picked in a file.
    # It has the following forms :
    # {%randint 0 10%} will generate a random number between 0 and 10
    # {%randstr 65 80 3%} will generate a random string of size 3 composed of characters between A and Z
    def parseExpression(self, expr: str) -> str:
        expressions = {
            "randint":self.parseRandInt,
            "randstr":self.parseRandStr,
            "choose":self.parseChoose
        }

        token = expr.split(' ')

        if token[0] in expressions:
            return expressions[token[0]](token)
        else:
            return ""


    # Takes a token in input.
    # If the token is a plain word, gets a random word from the corresponding file.
    # If the token is surrounded by %%, will try to parse an expression.
    # 
    # Will then check if there is a text attached to the token (a second element on the same row, in the CSV files)
    # And will parse it as a sentence.
    def parseToken(self, token: str) -> str:
        if(re.match("\%[a-z]+ [a-zA-Z0-9 ]+\%", token)):
            return self.parseExpression(token[1:-1])
        else:
            element = self.getRandomElementInFile(token)        
            result = element[0]
            modifier = None
            if len(element) > 1:
                modifier = element[1]
                self.currentItem.addModifier(result, self.parseSentence(modifier))        

            result = result[0].capitalize() + result[1:]

            return self.parseSentence(result)


    # Detects every token in a sentence, and calls the token parser to parse them        
    def parseSentence(self, sentence: str) -> str:
        ret = sentence
        for token in re.findall("{[a-zA-Z0-9% \\\/]+}", ret):
            ret = ret.replace(token, self.parseToken(token[1:-1]), 1)
        return ret
        

    def getItem(self) -> str:
        self.currentItem = Item()
        self.currentItem.name = self.getRandomElementInFile(self.formatFile)[0]

        self.currentItem.name = self.parseSentence(self.currentItem.name)

        return self.currentItem
