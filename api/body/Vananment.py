from .JWT import *

class PutVananment(PostJWT):
    content:str

class PostVananment(PostJWT):
    id:int
    content:str

class DeleteVananment(PostJWT):
    id:int