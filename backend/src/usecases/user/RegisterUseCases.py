from src.repositories.UserRepository import UserRepository
from src.domains.User import User
class InvalidUsername(ValueError):
    pass
class InvalidPassword(ValueError):
    pass
class AlreadyExists(ValueError):
    pass
class RegisterUseCase():
    def __init__(self,userRepository:UserRepository):
        self.userRepository=userRepository
    def execute(self,user:User)->bool:
        read_user= self.userRepository.getUser(user)
        if(read_user!=None):
            raise AlreadyExists("User already Exists")
        result=self.userRepository.registerUser(user)
        return result

