from fastapi import FastAPI
from app.config import settings
from app.auth.presentation.routes import router as auth_router

app = FastAPI(title=settings.app_name)

app.include_router(auth_router)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}
