from array import array
from typing import Optional
import os
import io
from src.dice.ast.Expression import Expression
from src.api.tokenizer import Tokenizer
from fastapi import FastAPI
# from src.dice.DiceParser import DiceParser
from src.dice2.DiceParser import DiceParser

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/dice/{expr}")
async def read_item(expr: str):
    tokenizer = Tokenizer(expr)
    parser = DiceParser(tokenizer.tokenize())
    parsed = parser.parse()
    if(not type(parsed) is Expression):
        return { 'status':400, 'result': parsed }
    else:
        return parsed


@app.get("/dice2/{expr}")
async def read_item(expr: str):
    p = DiceParser(debug=True, verbose=True)
    with io.StringIO() as f:
        f.write(expr)
        f.write('\0')
        f.seek(0)
        f.close()
        result = p.run(file='tmp.tmp', debug=False)
    return result
