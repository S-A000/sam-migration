from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.tasks.etl_engine import start_migration_task
from app.core.security import encrypt_db_password

router = APIRouter()

class MigrationRequest(BaseModel):
    job_name: str
    source_ip: str
    db_name: str
    db_user: str
    db_password: str
    destination_type: str # e.g., 'CSV' or 'S3'

@router.post("/start")
async def create_migration_job(request: MigrationRequest):
    try:
        # 1. Password ko Encrypt karein (Security Rule)
        encrypted_pass = encrypt_db_password(request.db_password)
        
        # 2. Job Metadata tayaar karein
        source_config = {
            "ip": request.source_ip,
            "db": request.db_name,
            "user": request.db_user,
            "pass": encrypted_pass
        }
        
        # 3. Background Task ko Trigger karein (Simulated Celery call)
        # Asal SaaS mein yahan 'delay()' use hota hai
        job_status = start_migration_task(
            job_id=101, # Future: DB se Auto-increment ID aayegi
            source_info=source_config,
            dest_info={"type": request.destination_type, "path": "cloud_data.csv"}
        )
        
        return {
            "status": "Job Started",
            "job_id": 101,
            "message": f"Migration '{request.job_name}' is now running in background."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))