from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db_control.database import get_db
from db_control import crud
from fastapi.responses import RedirectResponse
from db_control.models import AccessLog
from utils.timezone import jst_now
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter()

class AccessLogCreate(BaseModel):
    client_id: int
    zebra_id: str
    campaign_name: str
    uid: str
    target_url: str
    slug_prefix: str

@router.get("/")
def root():
    return {"status": "FastAPI fujiplus ready"}

@router.get("/track")
def track(uid: str, db: Session = Depends(get_db)):
    access_log = crud.update_access_log(db, uid)
    if not access_log:
        raise HTTPException(status_code=404, detail="UID not found")
    
    return RedirectResponse(url=access_log.target_url)

@router.get("/log")
def get_logs(
    zebra_id: str = Query(None),
    campaign_name: str = Query(None),
    target_url: str = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_all_logs(db, zebra_id=zebra_id, campaign_name=campaign_name, target_url=target_url)

@router.post("/log")
def create_log(
    uid: str = Query(...),
    client_id: int = Query(...),
    zebra_id: str = Query(...),
    campaign_name: str = Query(...),
    target_url: str = Query(...),
    slug_prefix: str = Query(...),
    db: Session = Depends(get_db)
):
     # ✅ ウォームアップリクエストかどうかを判定
    if zebra_id == "warmup":
        return {"slug": "warmup"}
    
    try:
        return crud.create_uid(
            db=db,
            client_id=client_id,
            zebra_id=zebra_id,
            campaign_name=campaign_name,
            uid=uid,
            target_url=target_url,
            slug_prefix=slug_prefix
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/bulk_log")
def bulk_create_log(
    logs: List[AccessLogCreate],
    db: Session = Depends(get_db)
):
    try:
        return crud.bulk_create_uids(db, [log.dict() for log in logs])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/track/{slug}")
def track_by_slug(slug: str, db: Session = Depends(get_db)):
    access_log = db.query(AccessLog).filter(AccessLog.slug == slug).first()
    if not access_log:
        raise HTTPException(status_code=404, detail="slug not found")
    
    access_log.access_count += 1
    access_log.last_accessed_at = jst_now()
    db.commit()

    return RedirectResponse(url=access_log.target_url)