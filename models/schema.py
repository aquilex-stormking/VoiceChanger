from datetime import date
from pydantic import BaseModel

# Create Patient Schema (Pydantic Model)
class PersonFoundCreate(BaseModel):
    firstname: str
    listofac: str
    listonu: str
    listfbi: str
    finddate: date
    consulta: str
    user:str

class PersonFound(BaseModel):
    id: int
    firstname: str
    listofac: str
    listonu: str
    listfbi: str
    finddate: date
    consulta: str
    user:str
    class Config:
        orm_mode = True


class UserFound(BaseModel):
    id: int
    firstname: str
    password: str
    email: str
    createdate: date
    state:str
    rol:str
    identificacion: int
    nit:int
    class Config:
        orm_mode = True

class UserFoundCreate(BaseModel):
    firstname: str
    password: str
    email: str
    createdate: date
    state:str
    rol:str
    identificacion: int
    nit:int
    # Orm Mode is used to support models that map to ORM objects, in this case model.Patient (sqlAlchemy)
    class Config:
        orm_mode = True

class UserDB(UserFoundCreate):
    password:str

class MatchFound(BaseModel):
    id: int
    observacion: str
    fecha: date
    resultado: str
    usuario: str
    consulta : str

    class Config:
        orm_mode = True    

class MatchFoundCreate(BaseModel):
    observacion: str
    fecha: date
    resultado: str
    usuario: str
    consulta: str

    class Config:
        orm_mode = True  

class List_addFound(BaseModel):
    id: int
    descripcion: str
    fecha: date
    fecha_ant:date
    class Config:
        orm_mode = True 
        
class List_addFoundCreate(BaseModel):
    descripcion: str
    fecha: date
    class Config:
        orm_mode = True  