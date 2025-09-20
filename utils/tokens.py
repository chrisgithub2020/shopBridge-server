import jwt
import os
import datetime
from typing import Any
from dotenv import load_dotenv
load_dotenv()


class JwtToken:
    secret_key = os.getenv("SECRET_KEY")
    def __init__(self) -> None:
        pass

    def create_token(self, payload: dict[str, Any], token_type: str):
        payload["exp"] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=7 if token_type == "access" else 31)
        payload["type"] = token_type
        token = jwt.encode(payload=payload, key=self.secret_key, algorithm="HS256")
        return token

    def verify_token(self, token):
        try:
            payload = jwt.decode(jwt=token, key=self.secret_key, algorithms="HS256")
            return {"success": True, "payload": payload}
        except jwt.ExpiredSignatureError:
            return {"success": False, "action": "refresh"} # we will use refresh token to refresh am
        except: ## for any error
            return {"success": False, "action": "login"}