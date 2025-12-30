from azure.cosmos import CosmosClient
import os
import azure.functions as func
from src.domains.User import User
from src.domains.Project import Project
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
from src.infrastructure.CosmosProjectRepository import CosmosProjectRepository
from src.usecases.project.DeleteProjectUseCase import DeleteProjectUseCase,ProjectDoesNotExist
import json
import logging
import datetime
bp= func.Blueprint()

@bp.route("delete-project",auth_level=func.AuthLevel.ANONYMOUS,methods=["POST"])
def deleteProject(req: func.HttpRequest)->func.HttpResponse:
    MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    AniMatesDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
    ProjectontainerProxy = AniMatesDBProxy.get_container_client(os.environ['ProjectContainerName'])

    logging.info(f"GOT AIPAC {req.get_json()}")
    try:
        project_data=req.get_json()
        projectRepository=CosmosProjectRepository(ProjectontainerProxy)
        projectName= project_data['name']
        deleteProjectUseCase= DeleteProjectUseCase(projectRepository)
        if(deleteProjectUseCase.execute(projectName)):
            return func.HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except ProjectDoesNotExist as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")
