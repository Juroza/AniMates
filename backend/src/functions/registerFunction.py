
from azure.cosmos import CosmosClient
import os
import azure.functions as func
from src.domains.User import User
from src.infrastructure.CosmosUserRepository import CosmosUserRepository
from src.usecases.RegisterUseCases import RegisterUseCase,AlreadyExists
import json
import logging
bp= func.Blueprint()

@bp.route("register",auth_level=func.AuthLevel.ANONYMOUS,methods=["POST"])
def registerUser(req: func.HttpRequest)->func.HttpResponse:
    MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    AniMatesDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
    UserContainerProxy = AniMatesDBProxy.get_container_client(os.environ['UserContainerName'])
    logging.info(f"GOT{req}")
    try:
        user_data=req.get_json()
        user= User(id=None,username=user_data["username"],password=user_data["password"])
        userRepository=CosmosUserRepository(UserContainerProxy)
        registerUseCase=RegisterUseCase(userRepository)
        if(registerUseCase.execute(user)):
            return func.HttpResponse(body=json.dumps({"result": True , "msg" : "OK"}),mimetype="application/json")
    except AlreadyExists as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")
