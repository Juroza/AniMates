from src.repositories.UserRepository import UserRepository
from src.domains.Frame import Frame
from src.repositories.ProjectRepository import ProjectRepository
from src.repositories.FrameRepository import FrameRepository
from src.domains.Project import Project
from typing import List
class FrameDoesNotExist(ValueError):
    pass
class DeleteFrameByNameUseCase():
    def __init__(self,frameRepository:FrameRepository):
        self.frameRepository=frameRepository
    def execute(self,frameName:str):
        frameRead=self.frameRepository.loadFrameByName(frameName)
        if(frameRead==None):
            raise FrameDoesNotExist
        self.frameRepository.deleteFrame(frameName)
        return True
        

