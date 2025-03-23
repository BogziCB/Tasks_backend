import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.routers import crud_operations
from database.db_connect import create_table

ROOT_PREFIX = "/api"
app = FastAPI(docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(crud_operations.router, prefix=f'{ROOT_PREFIX}')

if __name__ == "__main__":
    create_table()
    uvicorn.run(app, host="0.0.0.0", port=8080)