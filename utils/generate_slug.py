import hashlib

def generate_slug(prefix: str, uid: str) -> str:
    slug_hash = hashlib.sha256(uid.encode()).hexdigest()[:8]
    return f"{prefix}-{slug_hash}"