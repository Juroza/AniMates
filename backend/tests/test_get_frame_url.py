import unittest
import requests
import json


from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
from src.domains.User import User
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
class TestGetFrameUrl(unittest.TestCase): 
    LOCAL_DEV_URL="http://localhost:7071/get-frame-url"  
    TEST_URL = LOCAL_DEV_URL
    with open('backend/local.settings.json') as settings_file:
        settings = json.load(settings_file)
    MyCosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])
    UsersDBProxy = MyCosmos.get_database_client(settings['Values']['DatabaseName'])
    UserContainerProxy = UsersDBProxy.get_container_client(settings['Values']['UserContainerName'])
    userRepository= CosmosUserRepository(UserContainerProxy)
    def test_valid_get_frame_url(self):
        self.maxDiff=None
        response= requests.get(self.TEST_URL)
        self.assertEqual(200,response.status_code)
        print(response.json())
        response= requests.get(self.TEST_URL,params={"name":"1234.jpg"})
        self.assertEqual(200,response.status_code)
        print(response.json())
