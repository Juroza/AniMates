
from dataclasses import dataclass
import json
from typing import List
from .Project import Project
from .Stroke import Stroke
@dataclass
class Frame:
    def __init__(self,projectName:str,frameNumber:int,frameName:str,strokeRecord:List[Stroke]|None,id:str=""):
        self.projectName=projectName
        self.frameNumber=frameNumber
        self.strokeRecord=strokeRecord
        self.url=""
        self.frameName=frameName
        self.id=id
    def setStrokeRecord(self,strokeRecord:List[Stroke]):
        self.strokeRecord=strokeRecord
    def setName(self,name:str):
        self.frameName=name
    def setFrameNumber(self,num:int):
        self.frameNumber=num
    def to_dict(self):
        if self.strokeRecord:
            strokeRecordRep=[stroke.to_dict() for stroke in self.strokeRecord]
        else:
            strokeRecordRep=[]
        return {"projectName":self.projectName, "strokeRecord" :strokeRecordRep,"frameNumber":self.frameNumber,"frameName":self.frameName,"url":self.url,"id":self.id}
