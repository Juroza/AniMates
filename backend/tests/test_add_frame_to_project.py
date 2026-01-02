import datetime
import unittest
import requests
import json


from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError
from azure.cosmos import CosmosClient
from backend.src.domains.Project import Project
from backend.src.domains.Frame import Frame
from backend.src.domains.Stroke import Stroke,Segment,Point,strokeJsonParser
from backend.src.infrastructure.CosmosFrameRepository import CosmosFrameRepository
from backend.src.infrastructure.CosmosProjectRepository import CosmosProjectRepository
from src.domains.User import User
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
class TestAddFrameToProject(unittest.TestCase): 
    LOCAL_DEV_URL="http://localhost:7071/add-frame-to-project"  
    TEST_URL = LOCAL_DEV_URL
    with open('backend/local.settings.json') as settings_file:
        settings = json.load(settings_file)
    MyCosmos = CosmosClient.from_connection_string(settings['Values']['AzureCosmosDBConnectionString'])
    DBProxy = MyCosmos.get_database_client(settings['Values']['DatabaseName'])
    UserContainerProxy = DBProxy.get_container_client(settings['Values']['UserContainerName'])
    FrameContainerProxy = DBProxy.get_container_client(settings['Values']['FrameContainerName'])
    ProjectContainerProxy= DBProxy.get_container_client(settings['Values']['ProjectContainerName'])
    
    userRepository= CosmosUserRepository(UserContainerProxy)
    projectRepository= CosmosProjectRepository(ProjectContainerProxy)
    frameRepository= CosmosFrameRepository(FrameContainerProxy)
    def test_valid_add_frame(self):
        self.maxDiff=None
        owner=User(id=None,username="MyMy",password="Japsterdam")
        self.userRepository.deleteUser(owner)
        self.userRepository.registerUser(owner)
        member1=User(id=None,username="Coco",password="massaStudio")
        self.userRepository.deleteUser(member1)
        self.userRepository.registerUser(member1)
        member2=User(id=None,username="Maya",password="chudRage")
        self.userRepository.deleteUser(member2)
        self.userRepository.registerUser(member2)
        strokeJson='''{
    "segments": [
        {
            "point": {
                "x": 152.83338928222656,
                "y": 158.22222900390625
            },
            "time": 2.200000047683716,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 152.83338928222656,
                "y": 160.88888549804688
            },
            "time": 14.299999952316284,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 154.61111450195312,
                "y": 167.11111450195312
            },
            "time": 30.09999990463257,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 157.2777862548828,
                "y": 177.77780151367188
            },
            "time": 30.299999952316284,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 159.05555725097656,
                "y": 188.44444274902344
            },
            "time": 45.09999990463257,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 161.72222900390625,
                "y": 199.11111450195312
            },
            "time": 61.39999985694885,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 164.38888549804688,
                "y": 211.55555725097656
            },
            "time": 61.39999985694885,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 166.1666717529297,
                "y": 223.11111450195312
            },
            "time": 77.59999990463257,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 167.94444274902344,
                "y": 233.77780151367188
            },
            "time": 77.79999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 168.83338928222656,
                "y": 244.44447326660156
            },
            "time": 94.29999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 169.72222900390625,
                "y": 256
            },
            "time": 94.39999985694885,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 171.50006103515625,
                "y": 266.6667175292969
            },
            "time": 94.39999985694885,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 173.2777862548828,
                "y": 277.3333435058594
            },
            "time": 111.39999985694885,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 175.9445037841797,
                "y": 289.7778015136719
            },
            "time": 111.39999985694885,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 179.5,
                "y": 300.4444580078125
            },
            "time": 127.79999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 183.05555725097656,
                "y": 311.11114501953125
            },
            "time": 127.79999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 186.61111450195312,
                "y": 320.0000305175781
            },
            "time": 144.29999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 190.1666717529297,
                "y": 329.7778015136719
            },
            "time": 144.29999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 194.61111450195312,
                "y": 339.5555725097656
            },
            "time": 161.29999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 198.16671752929688,
                "y": 346.6667175292969
            },
            "time": 161.29999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 201.72222900390625,
                "y": 354.6666564941406
            },
            "time": 177.59999990463257,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 203.5,
                "y": 360
            },
            "time": 177.70000004768372,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 207.0556182861328,
                "y": 365.3334045410156
            },
            "time": 194.29999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 208.83338928222656,
                "y": 368.8888854980469
            },
            "time": 194.29999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 211.50006103515625,
                "y": 372.4444580078125
            },
            "time": 211,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 213.2777862548828,
                "y": 374.2222900390625
            },
            "time": 211.09999990463257,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 215.05555725097656,
                "y": 376
            },
            "time": 227.59999990463257,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 215.05555725097656,
                "y": 376.8888854980469
            },
            "time": 227.79999995231628,
            "pressure": 0.5
        },
        {
            "point": {
                "x": 215.05555725097656,
                "y": 376.8888854980469
            },
            "time": 343.89999985694885,
            "pressure": 0.5
        }
    ],
    "mode": "draw",
    "weight": 3,
    "smoothing": 0.85,
    "color": "000000",
    "adaptiveStroke": true
}'''

        project= Project("History Of Belgium",owner.username,True,[member1.username,member2.username])
        self.projectRepository.deleteProject(project)
        currentDateTime=datetime.datetime.now()
        project.setCreationDate(currentDateTime)
        self.projectRepository.createNewProject(project)
        stroke=strokeJsonParser(strokeJson)
        for s in stroke:

            print(s.to_dict())
        frame=Frame(project.projectName,1,"",stroke)

        response= requests.post(self.TEST_URL,json={"projectName":project.projectName,"strokeRecord":strokeJson,"frameNumber":1})
        self.assertEqual(200,response.status_code)
        projectRead=self.projectRepository.getProjectByName(project.projectName)
        self.assertEqual(projectRead.frameCount,1)
        frameRead=self.frameRepository.loadFrame(project.projectName,1)
        print(frameRead.strokeRecord)
        frame.setName(frameRead.frameName)
        print(frame.strokeRecord)
        self.assertEqual(frameRead.to_dict(),frame.to_dict())
        response= requests.post(self.TEST_URL,json={"projectName":project.projectName,"strokeRecord":strokeJson,"frameNumber":3})
        projectRead=self.projectRepository.getProjectByName(project.projectName)
        self.assertEqual(projectRead.frameCount,2)
        print(response.json())
