# backend/main.py
from fastapi import FastAPI
from backend.api import track
from backend.db_control import models
from backend.db_control.database import engine

# FastAPIインスタンス生成
app = FastAPI()

# データベース初期化（modelsとDBをバインド）
models.Base.metadata.create_all(bind=engine)

# ルーティング登録
app.include_router(track.router)