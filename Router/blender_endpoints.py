from fastapi import APIRouter, Depends, HTTPException
from db_models import BaseModel,engine,Viga
from sqlalchemy.orm import sessionmaker
from time import sleep
from fastapi import status
from models import Transform,Component,AddItem,updateItem,deleteItem
Session=sessionmaker(bind=engine,autoflush=True,autocommit=False)
router=APIRouter()
BaseModel.metadata.create_all(bind=engine)
db=Session()
@router.post("/transform")
async def transform(data:Transform):
    try:
        sleep(10)
        print(data)
        return data,status.HTTP_200_OK
    except Exception as e:
        return {"Message":"Unable to Get Data","status":status.HTTP_400_BAD_REQUEST}
@router.post("/translation")
async def translate(data:Component):
    try:
        sleep(10)
        print(data)
        return data,status.HTTP_200_OK
    except Exception as e:
        print(e)
        return {"Message":"Unable to Get Data","status":status.HTTP_400_BAD_REQUEST}
@router.post("/rotation")
async def rotation(data:Component):
    try:
        sleep(10)
        print(data)
        return data,status.HTTP_200_OK
    except Exception as e:
        print(e)
        return {"Message":"Unable to Get Data","status":status.HTTP_400_BAD_REQUEST}
@router.post("/scale")
async def scale(data:Component):
    try:
        sleep(10)
        print(data)
        return data,status.HTTP_200_OK
    except Exception as e:
        return {"Message":"Unable to Get Data","status":status.HTTP_400_BAD_REQUEST}
@router.post("/add-item")
async def add_item(item:AddItem):
    try:
        existing_item=db.query(Viga).filter(Viga.name == item.name).first() # query against name
        if existing_item:
            sleep(10)
            return {"Message":"Item Already Exists","status":status.HTTP_400_BAD_REQUEST}
        item=Viga(name=item.name,qty=item.qty)
        db.add(item) # Insert statement(DML)
        db.commit() # Transaction management(TCL)
        sleep(10)
        return {"Message":"Item Added","status":status.HTTP_200_OK}
    except Exception as e:
        return {"Message":"Unable to Add Item","status":status.HTTP_400_BAD_REQUEST}

@router.put("/update-item")
async def update_item(item:updateItem):
    try:
        obj=db.query(Viga).filter(Viga.name==item.name).first()
        if not obj:
            sleep(10)
            return {"Message":"Item Not Found","status":status.HTTP_404_NOT_FOUND}
        obj.qty=item.new_qty
        db.commit()
        sleep(10)
        return {"Message":"Item Updated","status":status.HTTP_200_OK}
    except Exception as e:
        return {"Message":"Unable to Update Item","status":status.HTTP_400_BAD_REQUEST}
@router.delete("/remove-item")
async def remove_item(item:deleteItem):
    try:
        obj=db.query(Viga).filter(Viga.name==item.name).first()
        if not obj:
            sleep(10)
            return {"Message":"Item Not Found","status":status.HTTP_404_NOT_FOUND}
        db.delete(obj)
        db.commit()
        sleep(10)
        return {"Message":"Item Removed","status":status.HTTP_200_OK}
    except Exception as e:
        return {"Message":"Unable to Remove Item","status":status.HTTP_400_BAD_REQUEST}