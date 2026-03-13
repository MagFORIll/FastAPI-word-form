import uvicorn
from fastapi import FastAPI
from app.API.endpoints.public_report_export import router

app = FastAPI()

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app=app)