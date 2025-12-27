from abc import ABC, abstractmethod
from src.domains.Project import Project
from src.domains.User import User
class ProjectRepository(ABC):
    @abstractmethod
    def createNewProject(self,project:Project):
        pass
    @abstractmethod
    def deleteProject(self,project:Project):
        pass
    @abstractmethod
    def getProject(self,id:str)->Project:
        pass
    @abstractmethod
    def setFPS(self,project:Project,fps:int):
        pass
    @abstractmethod
    def setUsers(self,project:Project,user:User):
        pass
