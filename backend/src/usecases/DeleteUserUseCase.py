from src.repositories.UserRepository import UserRepository
from src.domains.User import User
class InvalidUsername(ValueError):
    pass
class InvalidPassword(ValueError):
    pass
class InvalidUser(ValueError):
    pass
class DeleteUserUseCase():
    def __init__(self,userRepository:UserRepository):
        self.userRepository=userRepository
    def execute(self,user:User)->bool:
        read_user= self.userRepository.getUser(user)
        if(read_user==None):
            raise InvalidUser("User doesn't exist")
        result=self.userRepository.deleteUser(read_user)
        return result