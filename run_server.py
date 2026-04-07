import sys
import os
import uvicorn

# 1. Backend folder ka pura rasta Python ko batayein
backend_path = os.path.join(os.getcwd(), "backend")
sys.path.insert(0, backend_path)

if __name__ == "__main__":
    print(f"🚀 SaaS Engine starting from: {backend_path}")
    # 2. Server ko manually trigger karein
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)