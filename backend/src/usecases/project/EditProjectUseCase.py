from src.repositories.UserRepository import UserRepository
from src.domains.User import User
from src.repositories.ProjectRepository import ProjectRepository
from src.domains.Project import Project
class UserDoesNotExist(ValueError):
    pass
class ProjectDoesNotExist(ValueError):
    pass

class EditProjectUseCase():
    def __init__(self,projectRepository:ProjectRepository,userRepository:UserRepository):
        self.projectRepository=projectRepository
        self.userRepository=userRepository
    def execute(self,project:Project):
        allNonExistent=True
        invitedUsers=[]
        for user in project.users:
            invUser=self.userRepository.getUserByName(user)
            if(invUser!=None):
                allNonExistent=False
                invitedUsers.append(user)
        if(len(project.users)==0):
            allNonExistent=False
            
        if(allNonExistent):
            raise UserDoesNotExist("All users do not exist")
        projectRead=self.projectRepository.getProject(project.id)
        if(projectRead==None):
            raise ProjectDoesNotExist("Project Doesn't exist")
        
        users=set(project.users+invitedUsers)
        project.setInvitedUsers(users)
        self.projectRepository.updateProjectSettings(project)
        return True
        

