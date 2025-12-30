from src.repositories.UserRepository import UserRepository
from src.domains.User import User
from src.repositories.ProjectRepository import ProjectRepository
from src.domains.Project import Project
class ProjectDoesNotExist(ValueError):
    pass

class DeleteProjectUseCase():
    def __init__(self,projectRepository:ProjectRepository):
        self.projectRepository=projectRepository
    def execute(self,projectName:str):
        projectRead=self.projectRepository.getProjectByName(projectName)
        if(projectRead==None):
            raise ProjectDoesNotExist("Project Doesn't exist")
        self.projectRepository.deleteProject(projectRead)
        return True