import uvicorn
from app.fastapi_app import app

if __name__ == "__main__":
    uvicorn.run(
        "app.fastapi_app:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    ) 