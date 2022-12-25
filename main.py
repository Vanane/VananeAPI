from array import array
from multiprocessing.dummy import Array
from random import randint
import random
from typing import Optional
import os
import io
import json
import sys
from subprocess import Popen, PIPE
from urllib import response

# Configuration loader
import config

# FastAPI imports
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import RedirectResponse, ORJSONResponse

# For docs
from docs.openapi import SchemaBuilder

# Body models fot POST requests
from api.body.PostJWT import PostJWT
from api.body.PostAuthBody import PostAuthBody

from lib.db.DbManager import DbManager
from lib.auth.JWTManager import JWTManager

# Business classes
from api.item.itemGenerator import ItemGenerator
from lib.db.model.User import User


# Create FastAPI app
app = FastAPI(
    title = "VananeAPI",
    description = """
        Vanane API
        """,
    version = "0.5"
)


# Define the docs of the API with OpenAPI
schema = SchemaBuilder(app)
app.openapi = schema.build


#region Init

def initApp():
    # Init database manager
    first = False
    if not os.path.exists(config.config["Database"]["DB_PATH"]):
        first = True
    
    DbManager()
    
    if first:
        User.createUser(config.config["First User"]["USERNAME"], config.config["First User"]["PASSWORD"], ['ALL'], 1)

#endregion


# Initialize modules of the API
itemGenerator = ItemGenerator("api/item/data", "format")
initApp()

# region Endpoints

@app.get("/")
async def home():
    return RedirectResponse("/docs")


@app.get("/dice2/{expr}")
async def parse_dices(expr: str):
    diceProcess = Popen(args=["./api/dice2/bin/diceParser", expr], stdout=PIPE, stderr=PIPE)
    sys.stdout.flush()

    result = ""

    for line in iter(diceProcess.stdout.readline, b''):
        result += line.decode('ISO-8859-1')

    command = json.loads(result)

    if(type(command) == list):
        return command

    result = None
    try:
        result = makeCommand(command)
    except Exception as e:
        print("Caught error : " + e)
        result = makeError(e)
    return result


@app.get("/item")
async def get_item(howMany: Optional[int] = 1, seed: Optional[int] = None):
    if seed is None:
        seed = random.randint(-sys.maxsize, sys.maxsize)
    random.seed(seed)
    howMany = min(10, howMany)
    ret = [None] * howMany
    
    for i in range(0, howMany):
        ret[i] = itemGenerator.getItem()

    return ret

#region Vanane.net API

@app.post("/443/permissions")
async def post_permissions(body:PostJWT):
    if not JWTManager.checkJWT(body.jwt):
        raise HTTPException(status_code=403, detail="Invalid token, check /433/auth for more informations.")



@app.post("/443/auth")
async def post_auth(body:PostAuthBody):
    fail = False
    ret = None 
    
    if User.checkPassword(body.username, body.password):
        user = User.getUser(body.username)
        if user is not None:
            ret = JWTManager.getJWTForUser(user, duration=60)
        else:
            fail = True
    else:
        fail = True
    if fail:
        raise HTTPException(status_code=403, detail="Invalid credentials. This event will be logged.")
    return ret

#endregion

#endregion

#region Dice parsing 

def makeMult(command):
    result = []
    for i in range(0, command["left"]):
        result.append(makeCommand(command["right"]))
    return result


def makeAdd(command) -> int:
    leftResult = makeCommand(command["left"])
    rightResult = makeCommand(command["right"])    

    return leftResult[-1] + rightResult[-1]


def makeMod(command):
    return throwDice(command["left"]["left"], command["left"]["right"], command["right"])


def makeDice(command):
    print(command)
    return throwDice(command["left"], command["right"], 0)


def makeCommand(command):
    return {
        "mult": makeMult,
        "add": makeAdd,
        "mod": makeMod,
        "dice": makeDice
    }[command["type"]](command)   


def throwDice(count, value, bonus) -> array:
    results = []
    total = 0
    for i in range(0, count):
        results.append(randint(1, value) + bonus)
        total += results[i]
    if(count > 1):
        results.append(total)
    return results


def makeError(message):
    return {"type":"error", "value":message}


def checkErrors(command):
    if(type(command) is list): # The format of the error output of the dice parser is a JSON array, or list in Python
        return makeError(command[0]["value"])

#endregion
