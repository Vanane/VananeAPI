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
from config import config

# FastAPI imports
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

# For docs
from docs.openapi import SchemaBuilder

# Body models fot POST requests
from api.body.JWT import PostJWT
from api.body.Auth import PostAuth
from api.body.Vananment import *

# Response models, for autodoc
from api.response.Message import Message

from lib.db.DbManager import DbManager
from lib.auth.JWTManager import JWTManager
from lib.auth.PermManager import PermManager

# Business classes
from api.item.itemGenerator import ItemGenerator
from lib.db.model.User import User
from lib.db.model.Vananment import Vananment


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
    if not os.path.exists(config["Database"]["DB_PATH"]):
        first = True
    
    DbManager()
    
    if first:
        User.createUser(config["First User"]["USERNAME"], config["First User"]["PASSWORD"], [PermManager.adminPermission], 1)

#endregion


# Initialize modules of the API
itemGenerator = ItemGenerator("api/item/data", "format")
initApp()

#region Endpoints

@app.get("/", include_in_schema=False)
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


@app.post("/443/auth")
async def post_auth(body:PostAuth):
    fail = False
    ret = None 
    
    if User.checkPassword(body.username, body.password):
        user = User.getUser(body.username)
        ret = JWTManager.getJWTForUser(user)
    else:
        return JSONResponse(status_code=401, content = { "message":"Invalid credentials. This event will be logged." })
    return JSONResponse(status_code=200, content=ret)


@app.post("/443/permissions")
async def post_permissions(body:PostJWT):
    errorResponse = validateJWTAndPermissions(body.jwt, {})
    if errorResponse is not None:
        return errorResponse
    

    

@app.get("/443/test")
async def get_test():

    pass


#region Vananments

@app.get("/443/vananment")
async def get_vananments():
    res = Vananment.gets()
    return list(map(lambda x: x.toDict(), res))


@app.put("/443/vananment")
async def add_vananment(body:PutVananment):
    errorResponse = validateJWTAndPermissions(body.jwt, {"PutVananment"})
    if errorResponse is not None:
        return errorResponse
    return Vananment.add(body.content)


@app.post("/443/vananment")
async def modify_vananment(body:PostVananment):
    errorResponse = validateJWTAndPermissions(body.jwt, {"PostVananment"})
    if errorResponse is not None:
        return errorResponse

    vananment = Vananment.get(body.id)
    if vananment is None:
        return JSONResponse(status_code = 404, content = { "message" : "Vananment not found." })
    vananment.update(content = body.content)



@app.delete("/443/vananment")
async def delete_vananment(body:DeleteVananment):
    errorResponse = validateJWTAndPermissions(body.jwt, {"DeleteVananment"})
    if errorResponse is not None:
        return errorResponse

    vananment = Vananment.get(body.id)
    if vananment is None:
        return JSONResponse(status_code = 404, content = { "message" : "Vananment not found." })

    vananment.delete()
    

#endregion

#endregion

#endregion

#region Functions

def validateJWTAndPermissions(pJwt, perms:set):
    """
    If JWT is valid and user has the given permissions, returns None. Otherwise, returns a JSONResponse that can be returned to directly respond to the request.
    """
    decoded = JWTManager.validateAndDecodeJWT(pJwt)
    if decoded is None:
        return JSONResponse(status_code=401, content = {"message":"Invalid token, check /433/auth for more informations."})
    print((decoded))
    if not PermManager.hasPermissions(User.getUser(decoded['iss']), perms):
        return JSONResponse(status_code=403, content = {"message":"You are missing the following rights : " + str(perms)})

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

#endregion