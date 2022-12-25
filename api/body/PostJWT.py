from pydantic import BaseModel

class PostJWT(BaseModel):
    jwt:str
