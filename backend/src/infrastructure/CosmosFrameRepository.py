from typing import List
from azure.cosmos import ContainerProxy
from src.repositories.FrameRepository import FrameRepository
from src.domains.Project import Project
from src.domains.Frame import Frame
from src.domains.Stroke import Stroke,Segment,Point
from azure.cosmos.exceptions import CosmosResourceNotFoundError
class CosmosFrameRepository(FrameRepository):
    def __init__(self,container:ContainerProxy):
        self.container=container
    def storeFrame(self,frame):
        self.container.create_item(frame.to_dict(),enable_automatic_id_generation=True)
        return True
        
    
    def loadFrame(self, projectName: str, frameNumber: int):
        query = """
            SELECT * FROM c
            WHERE c.projectName = @name AND c.frameNumber = @n
        """

        params = [
            {"name": "@name", "value": projectName},
            {"name": "@n", "value": frameNumber},
        ]

        results = list(self.container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))

        # No frame found
        if not results:
            return None

        frame_data = results[0]

        strokeRecord: List[Stroke] = []

        for stroke in frame_data.get("strokeRecord", []):
            segments = stroke.get("segments", [])
            colour = stroke.get("colour", stroke.get("color", "#000000"))
            weight = int(stroke.get("weight", 1))
            smoothing = float(stroke.get("smoothing", 0.0))
            adaptiveStroke = bool(stroke.get("adaptiveStroke", False))

            strokeRec = Stroke(colour, weight, smoothing, adaptiveStroke)

            segmentReps: List[Segment] = []
            for segment in segments:
                p = segment.get("point", {})
                pointObj = Point(
                    float(p.get("x", 0.0)),
                    float(p.get("y", 0.0))
                )
                time = float(segment.get("time", 0.0))
                pressure = float(segment.get("pressure", 0.0))

                segRec = Segment(pointObj, time, pressure)
                segmentReps.append(segRec)

            strokeRec.setSegments(segmentReps)
            strokeRecord.append(strokeRec)

        return Frame(projectName, frameNumber,frame_data.get("frameName", "") ,strokeRecord,frame_data.get("id"))
    def loadFrameByName(self, frameName):
        query_result = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE c.frameName='{frameName}'",
        enable_cross_partition_query=True
        ))
        if(len(query_result)==0):
            return None

        if not query_result:
            return None

        return self._doc_to_frame(query_result[0])
    from typing import List

    def _doc_to_frame(self, doc: dict) -> Frame:
        # Basic frame fields
        projectName = doc.get("projectName", "")
        frameNumber = int(doc.get("frameNumber", 0))
        frameName = doc.get("frameName", "")
        id=doc.get("id")

        strokeRecords: List[Stroke] = []

        for stroke in doc.get("strokeRecord", []) or []:
            segments = stroke.get("segments", []) or []

            # handle both "colour" and "color"
            colour = stroke.get("colour", stroke.get("color", "#000000"))
            weight = int(stroke.get("weight", 1))
            smoothing = float(stroke.get("smoothing", 0.0))
            adaptiveStroke = bool(stroke.get("adaptiveStroke", False))

            strokeObj = Stroke(colour, weight, smoothing, adaptiveStroke)

            segmentObjs: List[Segment] = []
            for seg in segments:
                p = seg.get("point", {}) or {}
                pointObj = Point(
                    float(p.get("x", 0.0)),
                    float(p.get("y", 0.0)),
                )

                time = float(seg.get("time", 0.0))
                pressure = float(seg.get("pressure", 0.0))

                segmentObjs.append(Segment(pointObj, time, pressure))

            strokeObj.setSegments(segmentObjs)
            strokeRecords.append(strokeObj)

        frame = Frame(projectName, frameNumber, frameName, strokeRecords,id)

        # If you store url in Cosmos, bring it across
        if "url" in doc:
            frame.url = doc["url"]

        return frame

    def deleteFrame(self, frameName):
        results = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE c.frameName='{frameName}'",
        enable_cross_partition_query=True
        ))
        if(len(results)==0):
            return False
        for r in results:
            self.container.delete_item(r["id"], r["id"])
        return True
    def updateFrame(self, frame):
        print("a2")
        print("frameid")
        readFrame=self.container.read_item(item=frame.id,partition_key=frame.id)
        strokeRep=[]
        for stroke in frame.strokeRecord:
            strokeRep.append(stroke.to_dict())
        readFrame["strokeRecord"]=strokeRep
        readFrame["frameNumber"]=frame.frameNumber
        self.container.replace_item(readFrame["id"],readFrame)
        print("a4")
        return True