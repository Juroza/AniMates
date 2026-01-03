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
from src.usecases.frame.updateFrameDataUseCase import UpdateFrameeUseCase, FrameDoesNotExist
import json
import logging
import datetime
bp= func.Blueprint()

@bp.route("update-frame-data",auth_level=func.AuthLevel.ANONYMOUS,methods=["POST"])
def updateFrameByName(req: func.HttpRequest)->func.HttpResponse:
    MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    AniMatesDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
    ProjectContainerProxy = AniMatesDBProxy.get_container_client(os.environ['ProjectContainerName'])
    UserContainerProxy=  AniMatesDBProxy.get_container_client(os.environ['UserContainerName'])
    FrameContainerProxy=  AniMatesDBProxy.get_container_client(os.environ['FrameContainerName'])
    try:
        logging.info(f"GOT AIPAC {req.get_json()}")
        frameName = req.get_json()['name']
        strokeRecord= req.get_json()['strokeRecord']
        frameNumber= req.get_json()['frameNumber']
        frameRepository= CosmosFrameRepository(FrameContainerProxy)
        updateFrameUseCase=UpdateFrameeUseCase(frameRepository)
        strokeRec=strokeJsonParser(strokeRecord)
        if(updateFrameUseCase.execute(frameName,strokeRec,frameNumber)):
            return func.HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except FrameDoesNotExist as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")

