import uuid
import azure.functions as func
import json
import os
from datetime import datetime, timedelta, timezone
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
bp= func.Blueprint()
## Cutting corners with AI here mate, no time but works anyway
@bp.route("upload-frame",auth_level=func.AuthLevel.ANONYMOUS,methods=["POST"])
def uploadFrame(req: func.HttpRequest)->func.HttpResponse:
    try:
        # --- Inputs ---
        # filename is optional; if not provided, we generate one
        filename = req.params.get("filename")
        if not filename:
            filename = f"{uuid.uuid4().hex}.jpg"

        # Content-Type should be sent by the client (e.g. image/jpeg)
        content_type = req.headers.get("content-type", "application/octet-stream")

        # Raw bytes of the file
        data = req.get_body()
        if not data:
            return func.HttpResponse(
                json.dumps({"error": "Request body is empty. Send the image bytes as the request body."}),
                mimetype="application/json",
                status_code=400,
            )

        # --- Storage config ---
        account_name = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
        account_key = os.environ["AZURE_STORAGE_ACCOUNT_KEY"]
        container = os.environ.get("AZURE_STORAGE_CONTAINER", "frames")

        # Build a connection string from name+key (no need to store full conn string)
        conn_str = (
            "DefaultEndpointsProtocol=https;"
            f"AccountName={account_name};"
            f"AccountKey={account_key};"
            "EndpointSuffix=core.windows.net"
        )

        blob_service = BlobServiceClient.from_connection_string(conn_str)
        container_client = blob_service.get_container_client(container)

        # Ensure container exists (optional; remove if you manage containers manually)
        try:
            container_client.create_container()
        except Exception:
            pass  # already exists / no permission; ignore

        # Optional: make unique name to avoid collisions / caching issues
        # Keep extension if present
        ext = ""
        if "." in filename:
            ext = "." + filename.split(".")[-1].lower()
        blob_name = filename

        blob_client = container_client.get_blob_client(blob_name)

        # Upload
        blob_client.upload_blob(
            data,
            overwrite=False,
            content_settings=ContentSettings(content_type=content_type),
        )

        blob_url = f"https://{account_name}.blob.core.windows.net/{container}/{blob_name}"

        # OPTIONAL: generate a read SAS URL (useful because your storage blocks public access)
        sas = generate_blob_sas(
            account_name=account_name,
            container_name=container,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        read_url = f"{blob_url}?{sas}"

        return func.HttpResponse(
            json.dumps({
                "blobName": blob_name,
                "blobUrl": blob_url,
                "readUrl": read_url,  # use this in <img> if public access is disabled
                "contentType": content_type,
                "sizeBytes": len(data),
            }),
            mimetype="application/json",
            status_code=200,
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500,
        )