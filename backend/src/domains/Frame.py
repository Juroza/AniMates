
from dataclasses import dataclass
import json
from typing import List
from .Project import Project
from .Stroke import Stroke
@dataclass
class Frame:
    def __init__(self,project:Project,frameNumber:int,frameName:str,strokeRecord:List[Stroke]|None):
        self.project=project
        self.frameNumber=frameNumber
        self.strokeRecord=strokeRecord
        self.url=""
        self.frameName=frameName
    def setStrokeRecord(self,strokeRecord:List[Stroke]):
        self.strokeRecord=strokeRecord

    def to_dict(self):
        strokeRecordRep=[]
        for stroke in self.strokeRecord:
            strokeRecordRep.append(stroke.to_dict())
        return {"projectName":self.project.projectName, "projectOwner":  self.project.owner.id, "strokeRecord" :strokeRecordRep,"frameNumber":self.frameNumber,"frameName":self.frameName,"url":self.url}
