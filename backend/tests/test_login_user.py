import unittest
import requests
import json


from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
from src.domains.User import User
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
class TestLoginUser(unittest.TestCase): 
    LOCAL_DEV_URL="http://localhost:7071/login"  
    TEST_URL = LOCAL_DEV_URL
    with open('backend/local.settings.json') as settings_file:
        settings = json.load(settings_file)
    MyCosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])
    UsersDBProxy = MyCosmos.get_database_client(settings['Values']['DatabaseName'])
    UserContainerProxy = UsersDBProxy.get_container_client(settings['Values']['UserContainerName'])
    userRepository= CosmosUserRepository(UserContainerProxy)
    def test_valid_login_user(self):
        user=User(id=None,username="Reigen",password="salty")
        self.userRepository.deleteUser(user)
        self.userRepository.registerUser(user)
        inputUserWrong=User(id=None,username="Reigen",password="salty111")
        response= requests.post(self.TEST_URL,json=inputUserWrong.to_dict())
        self.assertEqual(200,response.status_code)
        self.assertEqual(response.json(),{"result" :False, "msg": "Username or password was incorrect" })
        inputUserRight=User(id=None,username="Reigen",password="salty")
        response= requests.post(self.TEST_URL,json=inputUserRight.to_dict())
        self.assertEqual(200,response.status_code)
        self.assertEqual(response.json(),{"result" :True, "msg": "OK" })
        inputUserWrong=User(id=None,username="apofjpaj",password="salty111")
        response= requests.post(self.TEST_URL,json=inputUserWrong.to_dict())
        self.assertEqual(200,response.status_code)
        self.assertEqual(response.json(),{"result" :False, "msg": "Username or password was incorrect" })
       