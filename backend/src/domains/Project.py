from dataclasses import dataclass
import json
from typing import List
from datetime import datetime
from .User import User
@dataclass
class Project:
    def __init__(self,name:str,owner_name:str,isPrivate:bool,users:List[str]=[],width:int=1980,height:int=1080,fps:int=10,dateCreated:datetime=datetime(1999, 1, 1,1,1,1,1),lastUpdate:datetime=datetime(1999, 1, 1,1,1,1,1),frameCount:int=0,):
        self.projectName=name
        self.owner=owner_name
        self.private=isPrivate
        self.users=users
        self.width=width
        self.height=height
        self.FPS=fps
        self.dateCreated=dateCreated
        self.latestUpdateTime=lastUpdate
        self.frameCount=frameCount
        self.id=''
    def setInvitedUsers(self,users:List[str]):
        self.users=users
    def setID(self,id:str):
        self.id=id
    def setFrameCount(self,frameCount:int):
        self.frameCount=frameCount
    def setCreationDate(self,creationDate:datetime):
        self.dateCreated=creationDate
    def setLatestUpdateTime(self,updateTime:datetime):
        self.latestUpdateTime=updateTime
    def setProjectName(self,name:str):
        self.projectName=name
    def setFPS(self,fps:int):
        self.FPS=fps
    def setWidth(self,width:int):
        self.width=width
    def setHeight(self,height:int):
        self.height=height
    def setPrivate(self,priv:bool):
        self.private=priv
    def to_dict(self):
        return {"id":self.id,"name":self.projectName,"owner":self.owner,"private":self.private,"users":self.users,"width":self.width,"height":self.height,"fps":self.FPS,"datetime_created":self.dateCreated.isoformat(),"datetime_modified":self.latestUpdateTime.isoformat(),"frameCount":self.frameCount}

