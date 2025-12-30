from src.repositories.UserRepository import UserRepository
from src.domains.User import User
from src.repositories.ProjectRepository import ProjectRepository
from src.domains.Project import Project
class ProjectAlreadyExists(ValueError):
    pass
class UserDoesNotExist(ValueError):
    pass
class CreateNewProjectUseCase():
    def __init__(self,projectRepository:ProjectRepository,userRepository:UserRepository):
        self.projectRepository=projectRepository
        self.userRepository=userRepository
    def execute(self,project:Project):
        ownername=self.userRepository.getUserByName(project.owner)
        if(ownername==None):
            raise UserDoesNotExist("Owner does not exist")
        for username in project.users:
            user=self.userRepository.getUserByName(username)
            if(user==None):
                raise UserDoesNotExist("User does not exist")
        proj=self.projectRepository.getProjectByName(project.projectName)
        if(proj!=None):
            raise ProjectAlreadyExists("Project Already Exists")
        self.projectRepository.createNewProject(project)
        return True
        

