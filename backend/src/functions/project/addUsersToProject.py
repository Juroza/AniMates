from azure.cosmos import CosmosClient
import os
import azure.functions as func
from src.domains.User import User
from src.domains.Project import Project
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
from src.infrastructure.CosmosProjectRepository import CosmosProjectRepository
from src.usecases.project.AddUsersToProjectsUseCase import AddUsersToProjectUseCase,ProjectDoesNotExist,UserDoesNotExist
import json
import logging
import datetime
bp= func.Blueprint()

@bp.route("add-users-to-project",auth_level=func.AuthLevel.ANONYMOUS,methods=["POST"])
def addUsersToProject(req: func.HttpRequest)->func.HttpResponse:
    MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    AniMatesDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
    ProjectContainerProxy = AniMatesDBProxy.get_container_client(os.environ['ProjectContainerName'])
    UserContainerProxy=  AniMatesDBProxy.get_container_client(os.environ['UserContainerName'])
    logging.info(f"GOT AIPAC {req.get_json()}")
    try:
        data=req.get_json()
        projectRepository=CosmosProjectRepository(ProjectContainerProxy)
        userRepository= CosmosUserRepository(UserContainerProxy)
        inputUsers= data['users']
        projectName=data['project-name']
        addUserToProjectUseCase= AddUsersToProjectUseCase(projectRepository,userRepository)
        if(addUserToProjectUseCase.execute(inputUsers,projectName)):
            return func.HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except ProjectDoesNotExist as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")
    except UserDoesNotExist as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")
   
