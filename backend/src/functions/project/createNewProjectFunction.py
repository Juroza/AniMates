from azure.cosmos import CosmosClient
import os
import azure.functions as func
from src.domains.User import User
from src.domains.Project import Project
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
from src.infrastructure.CosmosProjectRepository import CosmosProjectRepository
from src.usecases.project.CreateNewProjectUseCase import CreateNewProjectUseCase,UserDoesNotExist,ProjectAlreadyExists
import json
import logging
import datetime
bp= func.Blueprint()

@bp.route("create-new-project",auth_level=func.AuthLevel.ANONYMOUS,methods=["POST"])
def createNewProject(req: func.HttpRequest)->func.HttpResponse:
    MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    AniMatesDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
    UserContainerProxy = AniMatesDBProxy.get_container_client(os.environ['UserContainerName'])
    ProjectontainerProxy = AniMatesDBProxy.get_container_client(os.environ['ProjectContainerName'])

    logging.info(f"GOT AIPAC {req.get_json()}")
    try:
        project_data=req.get_json()
        userRepository=CosmosUserRepository(UserContainerProxy)
        projectRepository=CosmosProjectRepository(ProjectontainerProxy)
        project= Project(project_data['name'],project_data['owner'],project_data['private'],project_data['users'],project_data['width'],project_data['height'],project_data['fps'],datetime.datetime.strptime(project_data['datetime_created'],"%Y-%m-%dT%H:%M:%S.%f"),datetime.datetime.strptime(project_data['datetime_modified'],"%Y-%m-%dT%H:%M:%S.%f"),project_data['frameCount'])
        createNewProjectUseCase= CreateNewProjectUseCase(projectRepository,userRepository)
        if(createNewProjectUseCase.execute(project)):
            return func.HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except ProjectAlreadyExists as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")
    except UserDoesNotExist as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")
    