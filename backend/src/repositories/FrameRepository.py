from abc import ABC, abstractmethod
from src.domains.Project import Project
from src.domains.Frame import Frame
class FrameRepository(ABC):
    @abstractmethod
    def storeFrame(self,frame:Frame):
        pass
    @abstractmethod
    def loadFrame(self,projectName:str,frameNumber:int)->Frame:
        pass
    @abstractmethod
    def loadFrameByName(self,frameName:str)->Frame:
        pass
    @abstractmethod
    def deleteFrame(self,frame:Frame):
        pass
    @abstractmethod
    def updateFrameStrokeRecord(self,frame:Frame):
        pass
