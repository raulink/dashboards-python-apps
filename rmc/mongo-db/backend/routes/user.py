from fastapi import APIRouter, HTTPException
from backend.schemas.user import UserSchema, UpdateUserSchema
from backend.database.connection import db

from bson.objectid import ObjectId # Para utilizar la referencia de sus ids

router = APIRouter()

@router.post("/users/",response_model=UserSchema)
async def create_user(user:UserSchema):
    user_dict = user.dict() #Convertir en diccionario el objeto
    result = db['users'].insert_one(user_dict)
    user_dict['id'] = str(result.inserted_id)
    return user_dict

@router.get ("/users/{user_id}",response_model=UserSchema)
async def get_user(user_id:str):
    user = db['users'].find_one({"_id":ObjectId(user_id)})
    if user: 
        user['id'] = str(user['_id'])   #Se añade el id del usuario para visualizarlo
        return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")    # Si no se encuentra usuario se retorna error

@router.put ("/users/{user_id}",response_model=UserSchema)
async def update_user(user_id:str,user:UpdateUserSchema):
    updated_user = db['users'].find_one_and_update(
        {"_id":ObjectId(user_id)},
        {"$set":user.dict(exclude_unset=True)}, # Omitir el diccionario si no se encuentra id, creo
        return_document = True
    )
    if updated_user:
        updated_user['id'] = str(updated_user['_id'])   # Añade su id en lo que retorna
        return updated_user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete ("/users/{user_id}")
async def delete_user(user_id:str):
    result = db['users'].delete_one({"_id":ObjectId(user_id)})
    if result.deleted_count == 1: # Verificar la propiedad deleted_count
        return {"message":"Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
