from azure.cosmos import ContainerProxy
from src.repositories.UserRepository import UserRepository
from src.domains.User import User


class CosmosUserRepository(UserRepository):
    def __init__(self,container:ContainerProxy):
        self.container=container
    def registerUser(self, user:User):
        self.container.create_item(user.to_dict(),enable_automatic_id_generation=True)
        return True
    def getUser(self,user:User):
        query_result = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE c.username='{user.username}'",
        enable_cross_partition_query=True
        ))
        if(len(query_result)==0):
            return None
        user_data= query_result[0]
        user= User(user_data["id"],user_data["username"],user_data["password"])
        return user
    def getUserByName(self,username:str):
        query_result = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE c.username='{username}'",
        enable_cross_partition_query=True
        ))
        if(len(query_result)==0):
            return None
        user_data= query_result[0]
        user= User(user_data["id"],user_data["username"],user_data["password"])
        return user
    def deleteUser(self, user):
        results = list(self.container.query_items(
        query=f"SELECT * FROM c WHERE c.username='{user.username}'",
        enable_cross_partition_query=True
        ))
        if(len(results)==0):
            return False
        for r in results:
            self.container.delete_item(r["id"], r["id"])
        return True