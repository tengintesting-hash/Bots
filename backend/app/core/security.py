import hashlib
import hmac
from urllib.parse import parse_qsl

from fastapi import HTTPException, Header, status

from app.core.config import settings


def verify_telegram_init_data(init_data: str) -> dict:
    if not init_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Відсутні дані Telegram")

    data_check = dict(parse_qsl(init_data, strict_parsing=True))
    received_hash = data_check.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Відсутній хеш Telegram")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data_check.items()))
    secret_key = hashlib.sha256(settings.bot_token.encode("utf-8")).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалідні дані Telegram")

    return data_check


def verify_admin_token(x_admin_token: str | None = Header(default=None)) -> None:
    if not x_admin_token or x_admin_token != settings.admin_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалідний токен адміністратора")
