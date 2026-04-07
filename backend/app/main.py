from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# API Routers (Inko tabhi use karein jab files exist karti hon)
try:
    from app.api import auth, connections, jobs, websockets
except ImportError:
    print("Warning: API modules not found. Check app/api folder.")

app = FastAPI(title="ArchitectData - Enterprise Migration SaaS")

# --- 1. CORS Settings ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Path Handling (Absolute & Reliable) ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # backend/app
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR)) # Project Root
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

# --- 3. Jinja2 & Static Setup ---
templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "public"))

# Static files for CSS, JS, and Images
app.mount("/src", StaticFiles(directory=os.path.join(FRONTEND_DIR, "src")), name="src")
app.mount("/public", StaticFiles(directory=os.path.join(FRONTEND_DIR, "public")), name="public")

# --- 4. API Routers Inclusion ---
try:
    app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
    app.include_router(connections.router, prefix="/api/connections", tags=["Connections"])
    app.include_router(jobs.router, prefix="/api/jobs", tags=["Migration Jobs"])
    app.include_router(websockets.router, tags=["Live Streams"])
except Exception as e:
    print(f"Router inclusion error: {e}")

# --- 5. Page Routes (Jinja2 Rendering) ---

@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/manager")
async def serve_manager(request: Request):
    return templates.TemplateResponse("ConnectionManager.html", {"request": request})

@app.get("/monitor")
async def serve_monitor(request: Request):
    return templates.TemplateResponse("LiveMigrationManager.html", {"request": request})

@app.get("/billing")
async def serve_billing(request: Request):
    return templates.TemplateResponse("Billing&Health.html", {"request": request})

@app.get("/logs")
async def serve_logs(request: Request):
    return templates.TemplateResponse("LogsAndHealth.html", {"request": request})

@app.get("/signin")
async def serve_signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

# --- 6. Status API ---
@app.get("/api/status")
async def health_check():
    return {"status": "Online", "engine": "FastAPI", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)