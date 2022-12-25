from pydantic import BaseModel

class PostAuthBody(BaseModel):
    username:str
    password:str