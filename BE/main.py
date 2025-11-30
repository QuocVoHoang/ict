from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import devices, sensors, alerts, websocket
from app.config import settings
import asyncio
from kafka.consumer import consume

# Initialize FastAPI app
app = FastAPI(
    title="IoT Dashboard API",
    description="API for IoT Dashboard with device management, sensor data, and alerts",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(devices.router, prefix="/api/v1/devices", tags=["devices"])
app.include_router(sensors.router, prefix="/api/v1/sensors", tags=["sensors"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(websocket.router, prefix="/api/v1", tags=["websocket"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to IoT Dashboard API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event() -> None:
    """Start the background polling task on application startup."""
    # Kick off the polling task as a background task. It will run
    # indefinitely until the application shuts down. We deliberately
    # don't await the function to avoid blocking the startup sequence.
    asyncio.create_task(consume())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

