from pathlib import Path
import unittest
import requests
import json


from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
from src.domains.User import User
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
class TestUploadFrame(unittest.TestCase): 
    LOCAL_DEV_URL="http://localhost:7071/upload-frame"  
    TEST_URL = LOCAL_DEV_URL
    with open('backend/local.settings.json') as settings_file:
        settings = json.load(settings_file)
    MyCosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])
    UsersDBProxy = MyCosmos.get_database_client(settings['Values']['DatabaseName'])
    UserContainerProxy = UsersDBProxy.get_container_client(settings['Values']['UserContainerName'])
    userRepository= CosmosUserRepository(UserContainerProxy)
    def test_valid_upload_frame(self):
        test_blob_name = "12345.jpg"  # deterministic blob name


        img_path = Path(__file__).parent / "test_frames" / "Jaco_Pastorius_with_bass_1980.jpg"
        data = img_path.read_bytes()
        self.maxDiff=None
        response= requests.post(self.TEST_URL,data=data,params={"filename":test_blob_name})
        print(response.json())
