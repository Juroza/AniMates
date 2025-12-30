import unittest
import requests
import json
import datetime

from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
from src.domains.User import User
from src.domains.Project import Project
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
from src.infrastructure.CosmosProjectRepository import CosmosProjectRepository

class TestProject(unittest.TestCase):
    LOCAL_DEV_URL="http://localhost:7071/get-users-project"  
    LOCAL_DEV_Create_URL="http://localhost:7071/create-new-project"  
    TEST_URL = LOCAL_DEV_URL
    with open('backend/local.settings.json') as settings_file:
        settings = json.load(settings_file)
    MyCosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])
    DBProxy = MyCosmos.get_database_client(settings['Values']['DatabaseName'])
    UserContainerProxy = DBProxy.get_container_client(settings['Values']['UserContainerName'])
    ProjectContainerProxy= DBProxy.get_container_client(settings['Values']['ProjectContainerName'])
    userRepository= CosmosUserRepository(UserContainerProxy)
    projectRepository= CosmosProjectRepository(ProjectContainerProxy)
    def test__nbean(self):
        print(self.settings['Values']['AzureCosmosDBConnectionString'])
    def test_valid_create_new_project(self):
        self.maxDiff=None
        owner=User(id=None,username="Vera",password="wine")
        self.userRepository.deleteUser(owner)
        self.userRepository.registerUser(owner)
        member1=User(id=None,username="Coco",password="massaStudio")
        self.userRepository.deleteUser(member1)
        self.userRepository.registerUser(member1)
        member2=User(id=None,username="Maya",password="chudRage")
        self.userRepository.deleteUser(member2)
        self.userRepository.registerUser(member2)

        
        project= Project("Future Of Belgium",owner.username,True,[member1.username,member2.username])
        self.projectRepository.deleteProject(project)
        currentDateTime=datetime.datetime.now()
        project.setCreationDate(currentDateTime)
        response= requests.post(self.LOCAL_DEV_Create_URL,json=project.to_dict())
        self.assertEqual(200,response.status_code)
        projectColab= Project("Present Of Belgium",member1.username,True,[owner.username,member2.username])
        self.projectRepository.deleteProject(projectColab)
        currentDateTime=datetime.datetime.now()
        projectColab.setCreationDate(currentDateTime)
        response= requests.post(self.LOCAL_DEV_Create_URL,json=projectColab.to_dict())
        self.assertEqual(200,response.status_code)

        response= requests.post(self.TEST_URL,json={'name':owner.username})
        self.assertEqual(200,response.status_code)
        print(response.json())
        print(project.to_dict())
        print(projectColab.to_dict())
        self.assertEqual(response.json(),{"my-projects":[project.to_dict()],"collab-projects":[projectColab.to_dict()]})
       