from pydantic import BaseModel

class PostAuth(BaseModel):
    username:str
    password:str