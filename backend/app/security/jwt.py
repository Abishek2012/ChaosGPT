from datetime import datetime, timedelta, timezone
from jose import jwt

ALGORITHM = "HS256"

def create_access_token(subject: str, secret: str, roles: list[str], minutes: int = 30) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": subject, "roles": roles, "iat": now, "exp": now + timedelta(minutes=minutes)}, secret, algorithm=ALGORITHM)

def decode_access_token(token: str, secret: str) -> dict:
    return jwt.decode(token, secret, algorithms=[ALGORITHM])
