from fastapi import FastAPI

from app.auth.presentation.routes import router as auth_router
from app.shared.infrastructure.web.cors import configure_cors


app = FastAPI()

configure_cors(app)

app.include_router(auth_router)
