from dataclasses import dataclass
import json
from typing import List
from datetime import datetime
from User import User
from Frame import Frame
@dataclass
class Project:
    def __init__(self,name:str,owner_name:str,isPrivate:bool,users:List[str]=[],width:int=1980,height:int=1080,fps:int=10,dateCreated:datetime=datetime(1999, 1, 1),lastUpdate:datetime=datetime(1999, 1, 1),frameCount:int=0,):
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
    def setInvitedUsers(self,users:List[User]):
        self.users=users
    def setID(self,id:str):
        self.id=id
    def setFrameCount(self,frameCount:int):
        self.frameCount=frameCount
    def setCreationDate(self,creationDate:datetime):
        self.dateCreated=creationDate
    def setLatestUpdateTime(self,updateTime:datetime):
        self.latestUpdateTime=updateTime
    def to_dict(self):
        return {"name":self.projectName,"owner":self.owner,"private":self.private,"users":self.users,"frameCount":self.frameCount,"width":self.width,"height":self.height,"fps":self.FPS,"datetime_created":self.dateCreated.isoformat(),"datetime_modified":self.latestUpdateTime.isoformat()}

