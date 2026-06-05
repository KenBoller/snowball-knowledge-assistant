from fastapi import FastAPI

app = FastAPI(
    title="Snowball Knowledge Assistant",
    description="A FastAPI-powered RAG assistant for uploading documents and asking citation-backed questions.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Snowball Knowledge Assistant is alive."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }