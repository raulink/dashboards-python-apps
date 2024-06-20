from pydantic import BaseModel

class UserSchema (BaseModel):
    name:str
    email:str
    password:str

# Esquema para actualizar un usuario
class UpdateUserSchema(BaseModel):
    name: str = None
    email: str = None
    password: str = None