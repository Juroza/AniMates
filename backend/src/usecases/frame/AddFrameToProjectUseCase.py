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
        projectRead.frames = projectRead.frames or []
        
        # Insert the new frame's name into the frames list at the correct position
        inserted = False
        exists = False
        for i in range(len(projectRead.frames)):
            existing_frame_name = projectRead.frames[i]
            existing_frame = self.frameRepository.loadFrameByName(existing_frame_name)
            if existing_frame is None:
                continue
            if frame.frameNumber == existing_frame.frameNumber:
                # Skip adding
                exists = True
                inserted = True
                break
            if frame.frameNumber < existing_frame.frameNumber and not inserted:
                projectRead.frames.insert(i, frame.frameName)
                inserted = True
                break
        if not inserted:
            projectRead.frames.append(frame.frameName)
        if not exists:
            self.frameRepository.storeFrame(frame)
        
        projectRead.frameCount = len(projectRead.frames) 

        self.projectRepository.updateProjectSettings(projectRead)
        return True
        

