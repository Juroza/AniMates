from abc import ABC, abstractmethod
from src.domains.Project import Project
from src.domains.Frame import Frame
class FrameRepository(ABC):
    @abstractmethod
    def storeFrame(self,frame:Frame):
        pass
    @abstractmethod
    def loadFrame(self,project:Project,frameNumber:int)->Frame:
        pass
