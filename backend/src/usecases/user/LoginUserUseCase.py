from src.repositories.UserRepository import UserRepository
from src.domains.User import User
class InvalidUsername(ValueError):
    pass
class InvalidPassword(ValueError):
    pass
class AlreadyExists(ValueError):
    pass
class InvalidLogin(ValueError):
    pass
class LoginUserUseCase():
    def __init__(self,userRepository:UserRepository):
        self.userRepository=userRepository
    def execute(self,user:User)->bool:
        read_user= self.userRepository.getUser(user)
        if(read_user==None):
            raise InvalidLogin("Username or password was incorrect")
        
        if(user.password!=read_user.password):
            raise InvalidLogin("Username or password was incorrect")
        return True


