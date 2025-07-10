from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.auth import auth_router
from app.websocket import ws_router
from app.aiauth import ai_router
from app.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router)
app.include_router(ws_router)
app.include_router(ai_router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
