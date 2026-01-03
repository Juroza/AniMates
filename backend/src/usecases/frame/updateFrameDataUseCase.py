from src.repositories.UserRepository import UserRepository
from src.domains.Frame import Frame
from src.domains.Stroke import Stroke
from src.repositories.ProjectRepository import ProjectRepository
from src.repositories.FrameRepository import FrameRepository
from src.domains.Project import Project
from typing import List
class FrameDoesNotExist(ValueError):
    pass
class UpdateFrameeUseCase():
    def __init__(self,frameRepository:FrameRepository):
        self.frameRepository=frameRepository
    def execute(self,frameName:str,stroke:List[Stroke],frameNumber:int):
        frameRead=self.frameRepository.loadFrameByName(frameName)
        if(frameRead==None):
            raise FrameDoesNotExist
        frameRead.setStrokeRecord(stroke)
        frameRead.setFrameNumber(frameNumber)
        self.frameRepository.updateFrame(frameRead)
        return True
        

