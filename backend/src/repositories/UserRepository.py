from abc import ABC, abstractmethod
from typing import List
from src.domains.User import User
class UserRepository(ABC):
    @abstractmethod
    def registerUser(self,user:User)->bool:
        pass
    @abstractmethod
    def getUser(self,user:User)->User|None:
        pass
    @abstractmethod
    def getUserByName(self,user:User)->User|None:
        pass
    @abstractmethod
    def deleteUser(self,user:User)->bool:
        pass
    @abstractmethod
    def getAllUsers(self)->List[User]|None:
        pass
