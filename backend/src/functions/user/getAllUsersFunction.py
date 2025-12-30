
from azure.cosmos import CosmosClient
import os
import azure.functions as func
from src.domains.User import User
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
from src.usecases.user.GetAllUsersUseCase import GetAllUsersUseCase
import json
import logging
bp= func.Blueprint()

@bp.route("get-all-users",auth_level=func.AuthLevel.ANONYMOUS,methods=["POST"])
def getAllUsers(req: func.HttpRequest)->func.HttpResponse:
    MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    AniMatesDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
    UserContainerProxy = AniMatesDBProxy.get_container_client(os.environ['UserContainerName'])
    logging.info(f"GOT{req}")
    try:
        userRepository=CosmosUserRepository(UserContainerProxy)
        getAllUsersUseCase=GetAllUsersUseCase(userRepository)
        users=getAllUsersUseCase.execute()
        return func.HttpResponse(body=json.dumps(users),mimetype="application/json")
    except ValueError as e:
        return func.HttpResponse(body=json.dumps({"result":False , "msg" : e}),mimetype="application/json")