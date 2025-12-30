from src.repositories.UserRepository import UserRepository
from src.domains.User import User
from src.repositories.ProjectRepository import ProjectRepository
from src.domains.Project import Project
from typing import List
class UserDoesNotExist(ValueError):
    pass
class ProjectDoesNotExist(ValueError):
    pass
class AddUsersToProjectUseCase():
    def __init__(self,projectRepository:ProjectRepository,userRepository:UserRepository):
        self.projectRepository=projectRepository
        self.userRepository=userRepository
    def execute(self,usernames:List[str],projectName:str):
        allNonExistent=True
        invitedUsers=[]
        for user in usernames:
            invUser=self.userRepository.getUserByName(user)
            if(invUser!=None):
                allNonExistent=False
                invitedUsers.append(user)
        if(allNonExistent):
            raise UserDoesNotExist("All users do not exist")
        projectRead=self.projectRepository.getProjectByName(projectName)
        if(projectRead==None):
            raise ProjectDoesNotExist("Project Doesn't exist")
        
        users=set(projectRead.users+invitedUsers)
        projectRead.setInvitedUsers(users)
        self.projectRepository.updateProjectSettings(projectRead)
        return True
        

