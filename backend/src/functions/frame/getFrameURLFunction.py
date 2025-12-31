import azure.functions as func
import json
import os
from datetime import datetime, timedelta, timezone

from azure.storage.blob import generate_blob_sas, BlobSasPermissions
bp= func.Blueprint()

@bp.route("get-frame-url",auth_level=func.AuthLevel.ANONYMOUS,methods=["GET"])
def getFrameURL(req: func.HttpRequest)->func.HttpResponse:
    try:
        blob_name = req.params.get("name")
        if not blob_name:
            blob_name="i-guess-bro.jpg"
        account_name = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
        account_key = os.environ["AZURE_STORAGE_ACCOUNT_KEY"]
        container = os.environ["AZURE_FRAMES_CONTAINER"]

 
        blob_url = f"https://{account_name}.blob.core.windows.net/{container}/{blob_name}"

        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(hours=1),
        )

        read_url = f"{blob_url}?{sas_token}"

        return func.HttpResponse(body=json.dumps({"url": read_url}),mimetype="application/json")
    
    except Exception as e:
        return func.HttpResponse(json.dumps({"result":False,"msg":str(e)}),mimetype="application/json")
   