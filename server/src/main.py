from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth import router as auth_router  # Changed this line
from src.routes.profile import router as profile_router  # profile
from src.routes.subject import router as subject_router
from src.routes.resource import router as resource_router
from src.routes.progress import router as progress_router

app = FastAPI(
    title="Study App API",
    description="Backend API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add this line to include the router
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(subject_router)
app.include_router(resource_router)
app.include_router(progress_router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
