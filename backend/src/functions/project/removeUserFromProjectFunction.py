from azure.cosmos import CosmosClient
import os
import azure.functions as func
from src.domains.User import User
from src.domains.Project import Project
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
from src.infrastructure.CosmosProjectRepository import CosmosProjectRepository
from src.usecases.project.RemoveUsersFromProjects import RemoveUsersFromProjectUseCase,UserDoesNotExist
import json
import logging
import datetime
bp= func.Blueprint()

@bp.route("remove-users-from-project",auth_level=func.AuthLevel.ANONYMOUS,methods=["POST"])
def removeUserFromProject(req: func.HttpRequest)->func.HttpResponse:
    MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    AniMatesDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
    UserContainerProxy = AniMatesDBProxy.get_container_client(os.environ['UserContainerName'])
    ProjectontainerProxy = AniMatesDBProxy.get_container_client(os.environ['ProjectContainerName'])

    logging.info(f"GOT AIPAC {req.get_json()}")
    try:
        project_data=req.get_json()
        userRepository=CosmosUserRepository(UserContainerProxy)
        projectRepository=CosmosProjectRepository(ProjectontainerProxy)
        projectName=project_data['project-name']
        users=project_data['users']
        removeUserFromProjectUseCase= RemoveUsersFromProjectUseCase(projectRepository,userRepository)
        myProjRep=[]
        collabProjRep=[]
        removeUserFromProjectUseCase.execute(users,projectName)
        return func.HttpResponse(body=json.dumps({"my-projects":myProjRep,"collab-projects":collabProjRep}),mimetype="application/json")
    except UserDoesNotExist as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")
    