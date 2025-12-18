import unittest
import requests
import json


from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
from src.domains.User import User

class TestDeleteUser(unittest.TestCase): 
    LOCAL_DEV_URL="http://localhost:7071/delete"  
    DEPLOY_URL="https://animatesfunctions-dgfeb9ezcyaca6dz.francecentral-01.azurewebsites.net/delete"
    TEST_URL = LOCAL_DEV_URL
    with open('backend/local.settings.json') as settings_file:
        settings = json.load(settings_file)
    MyCosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])
    UsersDBProxy = MyCosmos.get_database_client(settings['Values']['DatabaseName'])
    UserContainerProxy = UsersDBProxy.get_container_client(settings['Values']['UserContainerName'])
    def test_valid_delete_user(self):
        user=User("12345","Iori","泣け！叫べ !そして、死ねぇ！")
        self.UserContainerProxy.create_item(user.to_dict(),enable_automatic_id_generation=True)
        response= requests.post(self.TEST_URL,json=user.to_dict())
        self.assertEqual(200,response.status_code)
        self.assertEqual(response.json(),{"result" : True, "msg": "OK" })
        query_result = list(self.UserContainerProxy.query_items(
    query=f"SELECT * FROM c WHERE c.username='{user.username}'",
    enable_cross_partition_query=True
))
        self.assertEqual(len(query_result),0)
    def test_deployed_valid_delete_user(self):
        user=User("12345789","Iori","泣け！叫べ !そして、死ねぇ！")
        self.UserContainerProxy.create_item(user.to_dict(),enable_automatic_id_generation=True)
        response= requests.post(self.DEPLOY_URL,json=user.to_dict())
        self.assertEqual(200,response.status_code)
        self.assertEqual(response.json(),{"result" : True, "msg": "OK" })
        query_result = list(self.UserContainerProxy.query_items(
    query=f"SELECT * FROM c WHERE c.username='{user.username}'",
    enable_cross_partition_query=True
))
        self.assertEqual(len(query_result),0)