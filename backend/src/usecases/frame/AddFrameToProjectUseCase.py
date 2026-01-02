from src.repositories.UserRepository import UserRepository
from src.domains.Frame import Frame
from src.repositories.ProjectRepository import ProjectRepository
from src.repositories.FrameRepository import FrameRepository
from src.domains.Project import Project
from typing import List
class UserDoesNotExist(ValueError):
    pass
class ProjectDoesNotExist(ValueError):
    pass
class AddFrameToProjectUseCase():
    def __init__(self,projectRepository:ProjectRepository,frameRepository:FrameRepository):
        self.projectRepository=projectRepository
        self.frameRepository=frameRepository
    def execute(self,frame:Frame,projectName:str):
        projectRead=self.projectRepository.getProjectByName(projectName)
        if(projectRead==None):
            raise ProjectDoesNotExist("Project Doesn't exist")
        self.frameRepository.storeFrame(frame)
        projectRead.frames = projectRead.frames or []
        projectRead.frames.append(frame.frameName)
        projectRead.frameCount = len(projectRead.frames) 

        self.projectRepository.updateProjectSettings(projectRead)
        return True
        

