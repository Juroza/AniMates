
from dataclasses import dataclass
import json
from typing import List
@dataclass
class Point:
    def __init__(self,x:float,y:float):
        self.x=x
        self.y=y
@dataclass
class Segment:
    def __init__(self,point:Point,time:int,presure:float):
        self.point=point
        self.time=time
        self.pressure=presure
    def to_dict(self):
        return {"point":self.point, "time":  self.time , "pressure" :self.pressure}

@dataclass
class Stroke:
    def __init__(self,colour:str,weight:int,smoothing:float,adaptiveStroke:bool):
        self.colour=colour
        self.weight=weight
        self.smoothing=smoothing
        self.adaptiveStroke=adaptiveStroke
    def setSegments(self,segments:List[Segment]):
        self.segments=segments

    def to_dict(self):
        segementsRep=[]
        for segment in self.segments:
            segementsRep.append(segment.to_dict())
        return {"segments":segementsRep , "colour":  self.colour , "weight" :self.weight,"smoothing":self.smoothing,"adaptiveStroke":self.adaptiveStroke}
