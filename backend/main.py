import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from auth import require_auth
from blob_reader import (
    read_latest_total_for_device,
    read_latest_totals_all_devices,
    read_historical_all_devices,
)

load_dotenv()

app = FastAPI(
    title="Energy Monitoring API",
    description="API for monitoring energy consumption from solar panels",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"[REQ] {request.method} {request.url.path}")
    resp = await call_next(request)
    return resp


# ============= PUBLIC ENDPOINTS =============

@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "status": "ok",
        "service": "Energy Monitoring API",
        "version": "1.0.0",
        "endpoints": {
            "profile": "/api/profile",
            "data": "/api/data",
            "history": "/api/history",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health")
def health():
    """Health check endpoint - verifies configuration"""
    config_ok = bool(
        os.getenv("COGNITO_ISSUER") and 
        os.getenv("COGNITO_CLIENT_ID") and
        os.getenv("AZURE_STORAGE_CONNECTION_STRING") and
        os.getenv("AZURE_BLOB_CONTAINER")
    )
    return {
        "status": "healthy" if config_ok else "degraded",
        "config_loaded": config_ok,
        "message": "All required environment variables are set" if config_ok else "Missing environment variables"
    }


# ============= PROTECTED ENDPOINTS =============

@app.get("/api/profile")
def profile(user=Depends(require_auth)):
    """Get current user profile"""
    return {
        "email": user["email"],
        "role": user["role"],
        "device_id": user["device_id"],
    }


@app.get("/api/data")
def data(user=Depends(require_auth)):
    """Get energy data - admin sees all devices, user sees only their device"""
    role = user.get("role")
    device_id = user.get("device_id")

    # ADMIN -> list all devices
    if role == "admin":
        items = read_latest_totals_all_devices()
        return {
            "role": role,
            "device_id": device_id,
            "data": items
        }

    # USER -> single device only
    if role == "user":
        if not device_id:
            raise HTTPException(
                status_code=403, 
                detail="No device_id claim for this user"
            )

        item = read_latest_total_for_device(device_id)
        return {
            "role": role,
            "device_id": device_id,
            "data": [item]
        }

    raise HTTPException(status_code=403, detail="Insufficient permissions")

@app.get("/api/history")
def history(user=Depends(require_auth), folders_limit: int = 2):
    """Get historical energy data - admin only"""
    role = user.get("role")

    if role == "admin":
        rows = read_historical_all_devices(
            folders_limit=folders_limit, 
            max_devices=50
        )
        return {
            "role": "admin", 
            "items": rows, 
            "count": len(rows)
        }
    
    if role == "user":
        raise HTTPException(
            status_code=403, 
            detail="Users cannot see history of devices"
        )
    
    raise HTTPException(status_code=403, detail="Insufficient permissions")


# Optional: Helper function for local testing (commented out in production)
# def fake_user():
#     return {"email": "local@test.com", "role": "admin", "device_id": "E-001"}