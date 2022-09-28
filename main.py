import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.database_config import Base, engine
from routers import product_router, auth_router, comments_router

app = FastAPI()

origins = {
    "http://localhost",
    "http://localhost:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router.router)
app.include_router(auth_router.router)
app.include_router(comments_router.router)
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8000, reload=True)
