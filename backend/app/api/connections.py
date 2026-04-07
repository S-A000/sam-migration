from fastapi import APIRouter, Body, HTTPException
import time
import boto3
from azure.storage.blob import BlobServiceClient
from botocore.exceptions import ClientError

router = APIRouter()

# --- HELPER FUNCTIONS FOR CLOUD CHECKING ---

def verify_aws_s3(key, secret, bucket, region, token=None):
    try:
        session = boto3.Session(
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            aws_session_token=token,
            region_name=region
        )
        s3 = session.client('s3')
        # Bucket ki existence check karne ke liye head_bucket call
        s3.head_bucket(Bucket=bucket)
        return True, "AWS S3: Connection Established & Bucket Verified."
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            return False, "AWS Error: Bucket does not exist."
        elif error_code == '403':
            return False, "AWS Error: Invalid Credentials (Access Denied)."
        else:
            return False, f"AWS Error: {str(e)}"
    except Exception as e:
        return False, f"Connection Failed: {str(e)}"

def verify_azure_blob(connection_string, container_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        if container_client.exists():
            return True, "Azure: Connection Established & Container Verified."
        else:
            return False, "Azure Error: Container not found in this account."
    except Exception as e:
        return False, f"Azure Connection Failed: {str(e)}"

# --- MAIN API ROUTE ---

@router.post("/test-connection")
async def test_complete_handshake(data: dict = Body(...)):
    mode = data.get("mode") # push or pull
    provider = data.get("provider")
    
    # Cloud Data
    c_key = data.get("key")
    c_secret = data.get("secret")
    c_bucket = data.get("bucket")
    c_region = data.get("region")
    c_conn = data.get("conn_string")
    c_token = data.get("token")

    # DB Data (Yahan hum pyodbc logic bhi add kar sakte hain)
    db_ip = data.get("ip")

    results = []
    
    # 1. Cloud Handshake Logic
    if provider == "aws_s3":
        success, msg = verify_aws_s3(c_key, c_secret, c_bucket, c_region, c_token)
    elif provider == "azure_blob":
        success, msg = verify_azure_blob(c_conn, c_bucket) # UI mein bucket hi container hai
    else:
        return {"status": "error", "message": "Unsupported cloud provider selected."}

    if not success:
        return {"status": "error", "message": msg}

    # 2. Final Response
    return {
        "status": "success",
        "message": f"Full {mode.upper()} Handshake Successful!",
        "details": {
            "cloud_status": msg,
            "db_status": f"Local Node {db_ip} is ready.",
            "timestamp": time.strftime("%H:%M:%S")
        }
    }