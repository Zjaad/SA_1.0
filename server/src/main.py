from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth import router as auth_router
from src.routes.profile import router as profile_router
from src.routes.subject import router as subject_router
from src.routes.resource import router as resource_router
from src.routes.progress import router as progress_router
from src.routes.schedule import router as schedule_router
from src.routes.study_block import router as study_block_router
from src.routes.tman import router as tman_router
from src.routes.notification import router as notification_router
from src.routes.tman_ai import router as tman_ai_router  # Changed this


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

# Router
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(subject_router)
app.include_router(resource_router)
app.include_router(progress_router)
app.include_router(schedule_router)
app.include_router(study_block_router)
app.include_router(tman_router)
app.include_router(notification_router)
app.include_router(tman_ai_router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "0.0.1"
    }
@app.get("/debug/routes")
async def debug_routes():
    routes = []
    for route in app.routes:
        routes.append(f"{route.methods} {route.path}")
    return routes
