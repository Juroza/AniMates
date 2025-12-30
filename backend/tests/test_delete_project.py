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
    LOCAL_DEV_Create_URL="http://localhost:7071/create-new-project"  
    LOCAL_DEV_URL="http://localhost:7071/delete-project"  
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
        owner=User(id=None,username="MyMy",password="Japsterdam")
        self.userRepository.deleteUser(owner)
        self.userRepository.registerUser(owner)
        member1=User(id=None,username="Coco",password="massaStudio")
        self.userRepository.deleteUser(member1)
        self.userRepository.registerUser(member1)
        member2=User(id=None,username="Maya",password="chudRage")
        self.userRepository.deleteUser(member2)
        self.userRepository.registerUser(member2)

        
        project= Project("History Of Japsterdam",owner.username,True,[member1.username,member2.username])
        self.projectRepository.deleteProject(project)
        currentDateTime=datetime.datetime.now()
        project.setCreationDate(currentDateTime)
        response= requests.post(self.LOCAL_DEV_Create_URL,json=project.to_dict())
        self.assertEqual(200,response.status_code)
        print(response.text)
        query_result = list(self.ProjectContainerProxy.query_items(
    query=f"SELECT * FROM c WHERE c.name='{project.projectName}'",
    enable_cross_partition_query=True
))
        result=query_result[0]
        self.assertEqual(result['name'],project.projectName)
        self.assertEqual(result['owner'],owner.username)
        self.assertEqual(result['users'],[member1.username,member2.username])
        self.assertEqual(result['datetime_created'],currentDateTime.isoformat())
        projectRead=self.projectRepository.getProjectByName(project.projectName)
        response= requests.post(self.TEST_URL,json={'name':projectRead.projectName})
        query_result = list(self.ProjectContainerProxy.query_items(
    query=f"SELECT * FROM c WHERE c.name='{projectRead.projectName}'",
    enable_cross_partition_query=True
       
))
        self.assertEqual(len(query_result),0)