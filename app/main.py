from fastapi import FastAPI
from app.api.v1.endpoints import router as main_router
from app.api.v1.auth import router as auth_router

# Create instance FASTAPI
app = FastAPI()

# Register API endpoints
app.include_router(main_router, prefix='/v1', tags=['v1'])
app.include_router(auth_router, prefix='/v1', tags=['v1'])
