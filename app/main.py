from fastapi import FastAPI
from api.health import router as health_router
from app.config import APP_NAME, APP_VERSION
from api.documents import router as documents_router
from api.ask import router as ask_router

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(ask_router)

@app.get("/")
def root():
    return {
        "message": f"{APP_NAME} is alive."
    }