from fastapi import APIRouter
import hashlib
import re

from utils.validators import ConsumerData, SellerData, singInData
from utils.tokens import JwtToken
from utils.database import DBManip
from utils.save_item_images import save_images, load_image

jwt_api = JwtToken()
db = DBManip()

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/consumer")
def signUp_consumer(data: ConsumerData):# -> dict[str, Any] | dict[str, bool]:
    acc_id = db.insert_user("consumer",data.firstName,data.lastName,data.phoneNumber,data.email, data.password, data.address)

    if acc_id == False: 
        return {"success":False}

    refresh_payload = {"id": acc_id, "acc_type": "consumer"}
    refresh_token = jwt_api.create_token(payload=refresh_payload, token_type="refresh")

    access_payload = {"id": acc_id, "name":data.firstName+" "+data.lastName, "address": data.address, "acc_type": "consumer"}
    access_token = jwt_api.create_token(payload=access_payload, token_type="access")

    return {"success": True, "r_token":refresh_token, "a_token":access_token}

@router.post("/seller")
def signUp_seller(data: SellerData):
    acc_result = db.insert_user("seller", data.firstName,data.lastName,data.phoneNumber, data.email, data.password, data.address,data.store_name, data.store_photo)
    if acc_result == False:
        return {"success": False}
    
    image = save_images(data.store_photo, acc_result[1])
    refresh_payload = {"id": acc_result[0], "acc_type": "seller"}
    access_payload = {"id":acc_result[0], "store_name":data.store_name, "name":data.firstName+" "+data.lastName, "acc_type": "seller"}

    refresh_token = jwt_api.create_token(payload=refresh_payload, token_type="refresh")
    access_token = jwt_api.create_token(payload=access_payload, token_type="access")    

    return {"success": True, "r_token":refresh_token, "a_token": access_token}


@router.post("/signIN")
def signIN(signInDetails: singInData):
    encoded_password = signInDetails.password.encode("utf8")
    passwordHash = hashlib.sha256(encoded_password).hexdigest()

    acc = db.signIN(signInDetails.identifier, signInDetails.acc_type)
    print(acc)

    ## if any issue is encountered
    if acc == False:
        return {"success":False}
    
    if passwordHash == acc.password:
        refresh_payload = {"id":acc.id, "acc_type": signInDetails.acc_type}
        access_payload = {"id":acc.id, "name": acc.firstName+" "+acc.lastName, "address":acc.address, "acc_type": signInDetails.acc_type}

        refresh_token = jwt_api.create_token(payload=refresh_payload, token_type="refresh")
        access_token = jwt_api.create_token(payload=access_payload, token_type="access")

        response = {"success": True, "r_token":refresh_token, "a_token":access_token}
        return response
    else:
        return {"success":False}