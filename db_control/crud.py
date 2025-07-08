# backend/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from db_control.models import AccessLog
from utils.timezone import jst_now
import random
import string
from utils.generate_slug import generate_slug

def generate_slug(prefix: str, uid: str):
    # slug例: kurando-abc123
    suffix = uid[:6]
    return f"{prefix.lower()}-{suffix}"

# UIDを新規登録する
def create_uid(db: Session, zebra_id: str, client_id:str, campaign_name: str, uid: str, target_url: str, slug_prefix: str):
    slug = generate_slug(slug_prefix, uid)
    access_log = AccessLog(
        zebra_id=zebra_id,
        client_id=client_id,
        campaign_name=campaign_name,
        uid=uid,
        target_url=target_url,
        slug=slug,
        access_count=0,
        last_accessed_at=None
    )
    db.add(access_log)
    db.commit()
    db.refresh(access_log)  # 登録後のオブジェクト更新
    return access_log

# UIDを元にアクセスカウントを1増やす
def update_access_log(db: Session, uid: str):
    access_log = db.query(AccessLog).filter(AccessLog.uid == uid).first()
    if access_log:
        access_log.access_count += 1
        access_log.last_accessed_at = jst_now()
        db.commit()
        db.refresh(access_log)
    return access_log

# 全アクセスログを取得（zebra_idまたはcampaign_nameで絞り込み可能）
def get_all_logs(db: Session, zebra_id: str = None, campaign_name: str = None, target_url: str = None):
    query = db.query(AccessLog)
    
    if zebra_id:
        query = query.filter(AccessLog.zebra_id == zebra_id)
    if campaign_name:
        query = query.filter(AccessLog.campaign_name == campaign_name)
    if target_url:
        query = query.filter(AccessLog.target_url == target_url)

    return query.all()

def bulk_create_uids(db: Session, logs: list):
    access_logs = []
    for log in logs:
        slug = generate_slug(log["slug_prefix"], log["uid"])
        access_logs.append(
            AccessLog(
                client_id=log["client_id"],
                zebra_id=log["zebra_id"],
                campaign_name=log["campaign_name"],
                uid=log["uid"],
                target_url=log["target_url"],
                slug=slug,
                access_count=0,
                last_accessed_at=None
            )
        )

    db.bulk_save_objects(access_logs)
    db.commit()

    return [{"uid": l.uid, "slug": l.slug} for l in access_logs]
