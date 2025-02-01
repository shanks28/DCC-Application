from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine=create_engine('sqlite:///./test.db',echo=True,connect_args={'check_same_thread':False})
BaseModel=declarative_base()
class Viga(BaseModel):
    __tablename__="viga_inventory"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    qty=Column(Integer,nullable=False)