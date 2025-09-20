from fastapi import Header
from typing import Annotated

from utils.tokens import JwtToken

jwt_api = JwtToken()

def verify_request(access_token: Annotated[str, Header()]):
    if access_token.strip() == "":
        return False, "no_token"
    
    result = jwt_api.verify_token(access_token)
    if result["success"] == False:
        if result["action"] == "refresh":
            return False, "refresh"
        else:
            return False, "login"
    
    return True, result["payload"]