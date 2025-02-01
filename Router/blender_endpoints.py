from fastapi import APIRouter, Depends, HTTPException
from db_models import BaseModel,engine
from sqlalchemy.orm import sessionmaker
from time import sleep
from fastapi import status
Session=sessionmaker(bind=engine,autoflush=True,autocommit=False)
router=APIRouter()
BaseModel.metadata.create_all(bind=engine)

@router.post("/transform")
async def transform(data:dict):
    try:
        sleep(10)
        print(data)
        return data,status.HTTP_200_OK
    except Exception as e:
        return {"Message":"Unable to Get Data","status":status.HTTP_400_BAD_REQUEST}
@router.post("/translation")
async def translate(data:dict):
    try:
        sleep(10)
        print(data)
        return data,status.HTTP_200_OK
    except Exception as e:
        return {"Message":"Unable to Get Data","status":status.HTTP_400_BAD_REQUEST}
@router.post("/")
async def root(data:dict):
    pass