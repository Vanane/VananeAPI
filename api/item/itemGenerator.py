from posixpath import relpath
import random
import re
import os


# Constants
DEFAULT_FORMAT_FILE = "itemFormat"


class ItemGenerator:
    words:dict
    relPath:str
    formatFile:str


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
            fileContents = open(self.relPath + "/" + file + ".csv", "r").read().split('\n')
            self.words[file] = fileContents
        else:
            fileContents = self.words[file]
        return fileContents[random.randint(0, len(fileContents) - 1)]

        
    def parseToken(self, token) -> str:
        ret = self.getRandomElementInFile(token)
        ret = ret[0].capitalize() + ret[1:]
        return self.parseSentence(ret)

        
    def parseSentence(self, sentence) -> str:
        ret = sentence
        for token in re.findall("{[a-zA-Z0-9]+}", ret):
            ret = ret.replace(token, self.parseToken(token[1:-1]), 1)
        return ret
        

    def getItem(self) -> str:
        format = self.getRandomElementInFile(self.formatFile)
        ret = self.parseSentence(format)
        return ret
