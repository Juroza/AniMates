from typing import List
from azure.cosmos import ContainerProxy
from src.repositories.FrameRepository import FrameRepository
from src.domains.Project import Project
from src.domains.Frame import Frame
from src.domains.Stroke import Stroke,Segment

class CosmosFrameRepository(FrameRepository):
    def __init__(self,container:ContainerProxy):
        self.container=container
    def storeFrame(self,frame):
        self.container.create_item(frame.to_dict(),enable_automatic_id_generation=True)
        return True
        
    def loadFrame(self, project, frameNumber):
        query_result = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE c.name='{project.projectName}'",
        enable_cross_partition_query=True
        ))
        if(len(query_result)==0):
            return None
        if(len(query_result)<frameNumber):
            return None
        frame_data= query_result[frameNumber-1]
        strokeRecords:List[Stroke]=[]
        for stroke in frame_data["strokeRecord"]:
            segments=stroke["segments"]
            colour=stroke["colour"]
            weight=stroke["weight"]
            smoothing=stroke["smoothing"]
            adaptiveStroke=stroke["adaptiveStroke"]
            strokeRec=Stroke(colour,weight,smoothing,adaptiveStroke)
            segmentReps:List[Segment]=[]
            for segment in segments:
                point=segment["point"]
                time=segment["time"]
                pressure=segment["pressure"]
                segRec=Segment(point,time,pressure)
                segmentReps.append(segRec)

            strokeRec.setSegments(segmentReps)
            strokeRecords.append(strokeRec)
        frame=Frame(project,frameNumber,strokeRecords)
        return frame