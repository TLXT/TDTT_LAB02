"""
To-Do App Backend API
FastAPI application with Firebase Authentication and Firestore
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.firebase_config import firebase_config
from app.routers import auth, tasks


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    To-Do App API với Firebase Authentication và Firestore Database
    
    ## Features
    * 🔐 Firebase Authentication
    * ✅ CRUD operations cho tasks
    * 📊 Task statistics
    * 🔒 User-specific data isolation
    
    ## Authentication
    Sử dụng Bearer token trong Authorization header:
    ```
    Authorization: Bearer <firebase_id_token>
    ```
    """
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "Welcome to To-Do App API 📝",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running"
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "to-do-app-backend",
        "version": settings.APP_VERSION,
        "firebase_initialized": firebase_config.db is not None
    }


# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup
    """
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📚 API docs available at: /docs")
    print(f"🔥 Firebase initialized: {firebase_config.db is not None}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown
    """
    print(f"👋 Shutting down {settings.APP_NAME}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )