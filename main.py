# backend/main.py
from fastapi import FastAPI
from api import track
from db_control import models
from db_control.database import engine

# FastAPIインスタンス生成
app = FastAPI()

# データベース初期化（modelsとDBをバインド）
models.Base.metadata.create_all(bind=engine)

# ルーティング登録
app.include_router(track.router)