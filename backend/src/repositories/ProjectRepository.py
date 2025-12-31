from abc import ABC, abstractmethod
from src.domains.Project import Project
from src.domains.User import User
from typing import List,Tuple
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
    def getProjectByName(self,name:str)->Project:
        pass
    @abstractmethod
    def getProjectsByUserName(self,name:str)->Tuple[List[Project],List[Project]]:
        pass
    @abstractmethod
    def setFPS(self,project:Project,fps:int):
        pass
    @abstractmethod
    def setUsers(self,project:Project,user:User):
        pass
    @abstractmethod
    def updateProjectSettings(self,project:Project):
        pass
