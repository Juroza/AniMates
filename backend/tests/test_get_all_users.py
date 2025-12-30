import unittest
import requests
import json


from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
from src.domains.User import User
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
class TestLoginUser(unittest.TestCase): 
    LOCAL_DEV_URL="http://localhost:7071/get-all-users"  
    TEST_URL = LOCAL_DEV_URL
    with open('backend/local.settings.json') as settings_file:
        settings = json.load(settings_file)
    MyCosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])
    UsersDBProxy = MyCosmos.get_database_client(settings['Values']['DatabaseName'])
    UserContainerProxy = UsersDBProxy.get_container_client(settings['Values']['UserContainerName'])
    userRepository= CosmosUserRepository(UserContainerProxy)
    def test_valid_get_all_users(self):
        self.maxDiff=None
        user=User(id=None,username="Reigen",password="salty")
        self.userRepository.deleteUser(user)
        self.userRepository.registerUser(user)
        user1=User(id=None,username="Reigen2",password="salty")
        self.userRepository.deleteUser(user1)
        self.userRepository.registerUser(user1)
        user2=User(id=None,username="Reigen3",password="salty")
        self.userRepository.deleteUser(user2)
        self.userRepository.registerUser(user2)
        response= requests.post(self.TEST_URL)
        self.assertEqual(200,response.status_code)
        print(response.json())
