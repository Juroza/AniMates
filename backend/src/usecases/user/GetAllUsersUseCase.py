from src.repositories.UserRepository import UserRepository
from src.domains.User import User
class GetAllUsersUseCase():
    def __init__(self,userRepository:UserRepository):
        self.userRepository=userRepository
    def execute(self)->bool:
        users=self.userRepository.getAllUsers()
        userRep=[]
        for user in users:
            userRep.append(user.to_dict())

        return userRep


