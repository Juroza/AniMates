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
from src.usecases.frame.LoadFrameByNameUseCase import LoadFrameByNameUseCase, FrameDoesNotExist
import json
import logging
import datetime
bp= func.Blueprint()

@bp.route("load-frame",auth_level=func.AuthLevel.ANONYMOUS,methods=["GET"])
def laodFrameByName(req: func.HttpRequest)->func.HttpResponse:
    MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    AniMatesDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
    ProjectContainerProxy = AniMatesDBProxy.get_container_client(os.environ['ProjectContainerName'])
    UserContainerProxy=  AniMatesDBProxy.get_container_client(os.environ['UserContainerName'])
    FrameContainerProxy=  AniMatesDBProxy.get_container_client(os.environ['FrameContainerName'])
    try:
        frameName = req.params.get("name")
        
        projectRepository=CosmosProjectRepository(ProjectContainerProxy)
        userRepository= CosmosUserRepository(UserContainerProxy)
        frameRepository= CosmosFrameRepository(FrameContainerProxy)
        loadFrameByNameUseCase=LoadFrameByNameUseCase(frameRepository)
        result=loadFrameByNameUseCase.execute(frameName).to_dict()
        return func.HttpResponse(body=json.dumps(result),mimetype="application/json")
    except FrameDoesNotExist as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")

