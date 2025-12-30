from src.repositories.UserRepository import UserRepository
from src.domains.User import User
from src.repositories.ProjectRepository import ProjectRepository
from src.domains.Project import Project
class UserDoesNotExist(ValueError):
    pass
class GetUsersProjectsUseCase():
    def __init__(self,projectRepository:ProjectRepository,userRepository:UserRepository):
        self.projectRepository=projectRepository
        self.userRepository=userRepository
    def execute(self,username:str):
        user=self.userRepository.getUserByName(username)
        if(user==None):
            raise UserDoesNotExist("User does not exist")
        
        result=self.projectRepository.getProjectsByUserName(username)
        return result
        

