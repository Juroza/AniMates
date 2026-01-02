
from dataclasses import dataclass
import json
from typing import List, Union
@dataclass
class Point:
    def __init__(self,x:float,y:float):
        self.x=x
        self.y=y
    def to_dict(self):
        return {"x":self.x,"y":self.y}
@dataclass
class Segment:
    def __init__(self,point:Point,time:int,pressure:float):
        self.point=point
        self.time=time
        self.pressure=pressure
    def to_dict(self):
        return {"point":self.point.to_dict(), "time":  self.time , "pressure" :self.pressure}

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




def _parse_single_stroke(data: dict) -> Stroke:
    colour = data.get("colour", data.get("color", "#000000"))
    weight = int(data.get("weight", 1))
    smoothing = float(data.get("smoothing", 0.0))
    adaptive = bool(data.get("adaptiveStroke", False))

    stroke = Stroke(
        colour=colour,
        weight=weight,
        smoothing=smoothing,
        adaptiveStroke=adaptive,
    )

    segments_in = data.get("segments", [])
    segments_out: List[Segment] = []

    for seg in segments_in:
        p = seg.get("point", {})
        point = Point(
            x=float(p.get("x", 0.0)),
            y=float(p.get("y", 0.0)),
        )
        time = float(seg.get("time", 0.0))
        pressure = float(seg.get("pressure", 0.0))

        segments_out.append(
            Segment(point=point, time=time, pressure=pressure)
        )

    stroke.setSegments(segments_out)
    return stroke


def strokeJsonParser(payload: Union[str, dict, list]) -> List[Stroke]:
    """
    Accepts:
      - JSON string
      - single stroke dict
      - list of stroke dicts

    Returns:
      - List[Stroke]
    """
    data = json.loads(payload) if isinstance(payload, str) else payload

    # Normalize to list
    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        raise TypeError("Payload must be a stroke object or list of stroke objects")

    strokes: List[Stroke] = []
    for stroke_data in data:
        strokes.append(_parse_single_stroke(stroke_data))

    return strokes