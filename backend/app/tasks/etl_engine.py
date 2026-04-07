import time
from connectors.sources.sql_server import SQLServerConnector
from connectors.destinations.csv_data_lake import CSVConnector

def start_migration_task(job_id, source_info, dest_info):
    """
    Yeh function background worker (Celery) chalayega.
    job_id: Database ID
    source_info: SQL Server credentials
    dest_info: CSV file path
    """
    print(f"🚀 Job {job_id}: Starting migration engine...")
    
    # 1. Initialize Connectors
    source = SQLServerConnector(source_info)
    destination = CSVConnector(dest_info)

    try:
        # 2. Extract Data (Small batches/chunks mein)
        data_generator = source.extract_in_chunks(batch_size=1000)

        for chunk in data_generator:
            # 3. Transform / Masking (Optional)
            # 4. Load
            destination.load(chunk)
            
            # 5. Update Progress (WebSocket ke zariye UI update karega)
            print(f"📦 Job {job_id}: Processed 1000 rows...")
            time.sleep(0.5) # Real-world feel ke liye

        return {"status": "SUCCESS", "job_id": job_id}

    except Exception as e:
        print(f"❌ Job {job_id} Failed: {str(e)}")
        return {"status": "FAILED", "error": str(e)}