from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
import urllib.parse

# --- Azure App Service の環境変数から読み込み ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# --- 検証（どれかが未設定なら強制終了） ---
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise EnvironmentError("環境変数（DB_USER, DB_PASSWORD, DB_HOST, DB_NAME）のいずれかが未設定です")

# --- URLエンコード ---
encoded_user = urllib.parse.quote_plus(DB_USER)
encoded_pw = urllib.parse.quote_plus(DB_PASSWORD)

# --- MySQL接続URLの構築 ---
DATABASE_URL = f"mysql+pymysql://{encoded_user}:{encoded_pw}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- SSL証明書のパス（App Serviceに配置しておく） ---
base_path = Path(__file__).resolve().parent
SSL_CERT_PATH = str(base_path / "DigiCertGlobalRootCA.crt.pem")

# --- SQLAlchemy エンジン作成（SSL付き） ---
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": SSL_CERT_PATH
        }
    }
)

# --- セッション作成 ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- FastAPI用の依存関係で使うセッション取得関数 ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
