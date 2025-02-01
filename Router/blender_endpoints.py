from fastapi import APIRouter, Depends, HTTPException
from db_models import BaseModel,engine,Viga
from sqlalchemy.orm import sessionmaker
from time import sleep
from fastapi import status
from models import Transform,Component,AddItem,updateItem,deleteItem
from typing import Optional
import os
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

@router.put("/update-quantity")
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
@router.get("/file-path")
async def get_file_path(projectpath:Optional[bool]=False):
    try:
        dcc_files=[i for i in os.listdir(os.getcwd()) if i.endswith(".blend")]
        dcc_file=os.path.join(os.getcwd(),dcc_files[0] if dcc_files else "")
        project_structure=os.path.dirname(dcc_file)
        sleep(10)
        return {"FilePath":dcc_file if projectpath else project_structure,"status":status.HTTP_200_OK}
    except Exception as e:
        return {"Message":"Unable to Get File Path","status":status.HTTP_400_BAD_REQUEST}
@router.get("/notify-blender")
async def notify_blender():
    try:
        all_objs=db.query(Viga).all()
        inventory=[{"name":item.name,"quantity":item.qty} for item in all_objs]
        return {"inventory":inventory,"status":status.HTTP_200_OK}

    except Exception as e:
        return {"Message":"Unable to Get Inventory","status":status.HTTP_400_BAD_REQUEST}
@router.get("/inventory")
async def inventory():
    try:
        inv=db.query(Viga).all()
        inv_list=[{"name":item.name,"quantity":item.qty} for item in inv]
        return inv_list
    except Exception as e:
        return {"Message":"Unable to Get Inventory","status":status.HTTP_400_BAD_REQUEST}