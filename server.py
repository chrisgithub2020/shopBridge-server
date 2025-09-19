from fastapi import FastAPI, Header, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Any
from database import DBManip
import hashlib
import re
from tokens import JwtToken

from validators import ConsumerData, ItemData, SellerData, restockData, orderActionData, orderData, singInData

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
db = DBManip()
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

@app.post("/sign_up_consumer")
def signUp_consumer(data: ConsumerData):# -> dict[str, Any] | dict[str, bool]:
    acc_id = db.insert_user("Consumers",data.firstName,data.lastName,data.phoneNumber,data.email, data.password, data.address)

    if acc_id == False: 
        return {"success":False}

    refresh_payload = {"id": acc_id, "acc_type": "consumer"}
    refresh_token = jwt_api.create_token(payload=refresh_payload, token_type="refresh")

    access_payload = {"id": acc_id, "name":data.firstName+" "+data.lastName, "address": data.address, "acc_type": "consumer"}
    access_token = jwt_api.create_token(payload=access_payload, token_type="access")

    return {"success": True, "r_token":refresh_token, "a_token":access_token}

@app.post("/sign_up_seller")
def signUp_seller(data: SellerData):
    acc_id = db.insert_user("Sellers", data.firstName,data.lastName,data.phoneNumber, data.email, data.password, data.address,data.store_name, data.store_photo)
    
    if acc_id == False:
        return {"success": False}
    
    refresh_payload = {"id": acc_id, "acc_type": "seller"}
    access_payload = {"id":acc_id, "store_name":data.store_name, "name":data.firstName+" "+data.lastName, "acc_type": "seller"}

    refresh_token = jwt_api.create_token(payload=refresh_payload, token_type="refresh")
    access_token = jwt_api.create_token(payload=access_payload, token_type="access")    

    return {"success": True, "r_token":refresh_token, "a_token": access_token}

@app.get("/getTodaysProducts")
def getHomepageProduct():
    items = db.get_today_items()
    return items

@app.post("/add_item_to_store")
def addItemToStore(data: ItemData, verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
        
    if verification[1]["acc_type"] != "seller":
        return status.HTTP_403_FORBIDDEN
    
    product_id = db.insert_product(data.itemSeller, data.itemImages,data.itemName,data.itemDescription, data.itemPrice, data.itemQuantity, data.itemMainCat, data.itemSubCat)
    return {"success": True, "data":{"id": product_id, "name": data.itemName, "quantity": data.itemQuantity, "price":data.itemPrice, "photo":data.itemImages[0]}, "description":data.itemDescription} if product_id != False else {"success":False}

@app.post("/restock_item")
def restockItem(data: restockData, verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
        
    if verification[1]["acc_type"] != "seller":
        return status.HTTP_403_FORBIDDEN

    result = db.restock(data.restockNumber, data.itemID)
    return result

@app.get("/take_down/{id}")
def TakeDown(id: str, verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
        
    if verification[1]["acc_type"] != "seller":
        return status.HTTP_403_FORBIDDEN

    return True

@app.get("/store_orders/{id}")
def get_store_orders(id: str, verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
        
    if verification[1]["acc_type"] != "seller":
        return status.HTTP_403_FORBIDDEN

    result = db.getStoreOrders(id)
    return {"success": True, "data": result} if result else {"success":False}

@app.get("/store_items/{id}")
def get_store_items(id: str, verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
        
    if verification[1]["acc_type"] != "seller":
        return status.HTTP_403_FORBIDDEN

    items = db.get_store_items(id)
    return {"success": True, "data":items} if items else {"success":False}

@app.get("/category/{mainCat}/{subCat}")
def getCategory(mainCat:str, subCat:str):
    subCategory = subCat.split(",")
    result = db.getCategories(mainCat, subCategory)
    return {"success":True, "data":result} if result else {"success":False}

@app.get("/get_cart_content/{cartlist}")
def getCartContent(cartlist:str, verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
    
    content = []
    items = cartlist.split(",")
    for id in items:
        details = db.get_cart_contents(id=id)
        if details:
            content.append(details[0])
    return {"success": True, "data": content}

@app.get("/getProductDetails/{ProductID}")
def getProductDetails(ProductID:str):
    item = db.get_product_details(ProductID)
    return {"success": True, "data": item} if item else {"success":False}

@app.post("/complete_order")
def completeOrder(orderDetails: orderData, verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
    
    result = db.completeOrder(orderDetails.product, orderDetails.address, orderDetails.consumer, orderDetails.amountPaid, orderDetails.quantity)
    return {"success": True, "data": orderDetails} if result else {"success":False}

@app.post("/signIN")
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
    
    if passwordHash == acc[5]:
        refresh_payload = {"id":acc[0], "acc_type": signInDetails.acc_type}
        access_payload = {"id":acc[0], "name": acc[1]+" "+acc[2], "address":acc[6], "acc_type": signInDetails.acc_type}

        refresh_token = jwt_api.create_token(payload=refresh_payload, token_type="refresh")
        access_token = jwt_api.create_token(payload=access_payload, token_type="access")
        return {"success": True, "r_token":refresh_token, "a_token":access_token}
    else:
        return {"success":False}


@app.get("/searchProduct/{filter}")
def searchProduct(filter: str):
    result = db.searchProduct(filter)
    return {"success": True, "data": result} if result else {"success":False}

@app.post("/order_actions")
def orderActions(action: orderActionData):
    db.orderAction(action.id, action.action)
    return {"success": True, "data":True}

@app.get("/order_status/{id}")
def orderStatus(id: str):
    response = db.orderStatus(id=id)
    return {"success": response}