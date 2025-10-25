from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    
class UserGoogleCreate(BaseModel):
    name: str
    email: str
    
class UserLogin(BaseModel):
    email: str
    password: str
    
