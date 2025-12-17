import unittest
import requests
import json


from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
from src.domains.User import User
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
class TestRegisterUser(unittest.TestCase): 
    LOCAL_DEV_URL="http://localhost:7071/register"  
    TEST_URL = LOCAL_DEV_URL
    with open('backend/local.settings.json') as settings_file:
        settings = json.load(settings_file)
    MyCosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])
    UsersDBProxy = MyCosmos.get_database_client(settings['Values']['DatabaseName'])
    UserContainerProxy = UsersDBProxy.get_container_client(settings['Values']['UserContainerName'])
    userRepository= CosmosUserRepository(UserContainerProxy)
    def test_valid_register_player(self):
        user=User(id=None,username="Reigen",password="saltysplashy")
        self.userRepository.deleteUser(user)
        print("yooooo")
        print(user.id)
        response= requests.post(self.TEST_URL,json=user.to_dict())
        self.assertEqual(200,response.status_code)
        self.assertEqual(response.json(),{"result" : True, "msg": "OK" })
        query_result = list(self.UserContainerProxy.query_items(
    query=f"SELECT * FROM c WHERE c.username='{user.username}'",
    enable_cross_partition_query=True
))[0]

        query_result_stripped = {"username": query_result['username'],"password":query_result['password'] }
        self.assertEqual(query_result['username'],user.username)
        self.assertEqual(query_result['password'],user.password)