from fastapi import APIRouter
import hashlib
import re

from utils.validators import ConsumerData, SellerData, singInData
from utils.tokens import JwtToken
from utils.database import DBManip

jwt_api = JwtToken()
db = DBManip()

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/consumer")
def signUp_consumer(data: ConsumerData):# -> dict[str, Any] | dict[str, bool]:
    acc_id = db.insert_user("Consumers",data.firstName,data.lastName,data.phoneNumber,data.email, data.password, data.address)

    if acc_id == False: 
        return {"success":False}

    refresh_payload = {"id": acc_id, "acc_type": "consumer"}
    refresh_token = jwt_api.create_token(payload=refresh_payload, token_type="refresh")

    access_payload = {"id": acc_id, "name":data.firstName+" "+data.lastName, "address": data.address, "acc_type": "consumer"}
    access_token = jwt_api.create_token(payload=access_payload, token_type="access")

    return {"success": True, "r_token":refresh_token, "a_token":access_token}

@router.post("/seller")
def signUp_seller(data: SellerData):
    acc_id = db.insert_user("Sellers", data.firstName,data.lastName,data.phoneNumber, data.email, data.password, data.address,data.store_name, data.store_photo)
    
    if acc_id == False:
        return {"success": False}
    
    refresh_payload = {"id": acc_id, "acc_type": "seller"}
    access_payload = {"id":acc_id, "store_name":data.store_name, "name":data.firstName+" "+data.lastName, "acc_type": "seller"}

    refresh_token = jwt_api.create_token(payload=refresh_payload, token_type="refresh")
    access_token = jwt_api.create_token(payload=access_payload, token_type="access")    

    return {"success": True, "r_token":refresh_token, "a_token": access_token}


@router.post("/signIN")
def signIN(signInDetails: singInData):
    identifierType = None
    encoded_password = signInDetails.password.encode("utf8")
    passwordHash = hashlib.sha256(encoded_password).hexdigest()

    phone_re = re.compile("^\+?(\d{1,3})?[-.\s]?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})$")
    email_re = re.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    if (bool(phone_re.match(signInDetails.identifier.strip()))) == True:
        identifierType = "contact"
    if bool(email_re.match(signInDetails.identifier.strip())) == True:
        identifierType = "email"
    acc = db.signIN(identifierType, signInDetails.identifier, "Sellers" if signInDetails.acc_type == "seller" else "Consumers")

    ## if any issue is encountered
    if acc == False:
        return {"success":False}
    
    if passwordHash == passwordHash:
        refresh_payload = {"id":acc[0], "acc_type": signInDetails.acc_type}
        access_payload = {"id":acc[0], "name": acc[1]+" "+acc[2], "address":acc[6], "acc_type": signInDetails.acc_type}

        refresh_token = jwt_api.create_token(payload=refresh_payload, token_type="refresh")
        access_token = jwt_api.create_token(payload=access_payload, token_type="access")
        return {"success": True, "r_token":refresh_token, "a_token":access_token}
    else:
        return {"success":False}