import uuid
from azure.cosmos import CosmosClient
import os
import azure.functions as func
from src.domains.User import User
from src.domains.Project import Project
from src.domains.Stroke import strokeJsonParser
from src.domains.Frame import Frame
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
from src.infrastructure.CosmosProjectRepository import CosmosProjectRepository
from src.infrastructure.CosmosFrameRepository import CosmosFrameRepository
from src.usecases.frame.AddFrameToProjectUseCase import AddFrameToProjectUseCase,ProjectDoesNotExist
import json
import logging
import datetime
bp= func.Blueprint()

@bp.route("add-frame-to-project",auth_level=func.AuthLevel.ANONYMOUS,methods=["POST"])
def addFrameToProject(req: func.HttpRequest)->func.HttpResponse:
    MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    AniMatesDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
    ProjectContainerProxy = AniMatesDBProxy.get_container_client(os.environ['ProjectContainerName'])
    UserContainerProxy=  AniMatesDBProxy.get_container_client(os.environ['UserContainerName'])
    FrameContainerProxy=  AniMatesDBProxy.get_container_client(os.environ['FrameContainerName'])
    logging.info(f"GOT AIPAC {req.get_json()}")
    try:
        data=req.get_json()
        strokeData=strokeJsonParser(data["strokeRecord"])
        projectName=data["projectName"]
        frameNumber=data["frameNumber"]
        name=uuid.uuid4().hex
        frame=Frame(projectName,frameNumber,name,strokeData)
        
        projectRepository=CosmosProjectRepository(ProjectContainerProxy)
        userRepository= CosmosUserRepository(UserContainerProxy)
        frameRepository= CosmosFrameRepository(FrameContainerProxy)
        addFrameToProjectUseCase=AddFrameToProjectUseCase(projectRepository,frameRepository)
        if(addFrameToProjectUseCase.execute(frame,projectName)):
            return func.HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except ProjectDoesNotExist as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")

