from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import DBManip
import hashlib
import re
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

db = DBManip()


class ConsumerData(BaseModel):
    firstName:  str
    lastName: str
    email: str
    password: str
    phoneNumber: str
    address: str
    type: str


class SellerData(BaseModel):
    firstName:  str
    lastName: str
    email: str
    password: str
    phoneNumber: str
    address: str
    store_name: str
    store_photo: list
    type: str

class ItemData(BaseModel):
    itemSeller: str
    itemImages: list
    itemDescription: str
    itemName: str
    itemPrice: str
    itemQuantity: str
    itemSubCat: str

class orderData(BaseModel):
    consumer: str
    product: str
    amountPaid: float
    address: str
    quantity: str


class singInData(BaseModel):
    identifier: str
    password: str

class restockData(BaseModel):
    itemID: str
    restockNumber: str

class orderActionData(BaseModel):
    id: str
    action:str

@app.post("/sign_up_consumer")
def signUp_consumer(data: ConsumerData):
    acc_id = db.insert_user("Consumers",data.firstName,data.lastName,data.phoneNumber,data.email, data.password, data.address)
    return {"success": True, "id":acc_id} if acc_id != False else {"success":False}

@app.post("/sign_up_seller")
def signUp_seller(data: SellerData):
    acc_id = db.insert_user("Sellers",data.firstName,data.lastName,data.phoneNumber, data.email, data.password, data.address,data.store_name,data.store_photo)
    return {"success": True, "id":acc_id} if acc_id != False else {"success":False}

@app.get("/getTodaysProducts")
def getHomepageProduct():
    items = db.get_today_items()
    return items

@app.post("/add_item_to_store")
def addItemToStore(data: ItemData):
    product_id = db.insert_product(data.itemSeller, data.itemImages,data.itemName,data.itemDescription, data.itemPrice, data.itemQuantity, data.itemMainCat, data.itemSubCat)
    return {"success": True, "data":{"id": product_id, "name": data.itemName, "quantity": data.itemQuantity, "price":data.itemPrice, "photo":data.itemImages[0]}, "description":data.itemDescription} if product_id != False else {"success":False}

@app.post("/restock_item")
def restockItem(data: restockData):
    result = db.restock(data.restockNumber, data.itemID)
    return result

@app.get("/take_down/{id}")
def TakeDown(id: str):
    return True

@app.get("/store_orders/{id}")
def get_store_orders(id: str):
    result = db.getStoreOrders(id)
    return {"success": True, "data": result} if result else {"success":False}

@app.get("/store_items/{id}")
def get_store_items(id: str):
    items = db.get_store_items(id)
    return {"success": True, "data":items} if items else {"success":False}

@app.get("/category/{mainCat}/{subCat}")
def getCategory(mainCat:str, subCat:str):
    subCategory = subCat.split(",")
    result = db.getCategories(mainCat, subCategory)
    return {"success":True, "data":result} if result else {"success":False}

@app.get("/get_cart_content/{cartlist}")
def getCartContent(cartlist:str):
    content = []
    cartlist = cartlist.split(",")
    for id in cartlist:
        details = db.get_cart_contents(id=id)
        content.append(details[0])
    return {"success": True, "data": content}

@app.get("/getProductDetails/{ProductID}")
def getProductDetails(ProductID:str):
    item = db.get_product_details(ProductID)
    return {"success": True, "data": item} if item else {"success":False}

@app.post("/complete_order")
def completeOrder(orderDetails: orderData):
    result = db.completeOrder(orderDetails.product, orderDetails.address, orderDetails.consumer, orderDetails.amountPaid, orderDetails.quantity)
    return {"success": True, "data": orderDetails} if result else {"success":False}

@app.post("/signIN")
def signIN(signInDetails:singInData):
    identifierType = None
    encoded_password = signInDetails.password.encode("utf8")
    passwordHash = hashlib.sha256(encoded_password).hexdigest()
    phone_re = re.compile("^\+?(\d{1,3})?[-.\s]?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})$")
    email_re = re.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    if (bool(phone_re.match(signInDetails.identifier.strip()))) == True:
        identifierType = "p"
    if bool(email_re.match(signInDetails.identifier.strip())) == True:
        identifierType = "e"
    acc = db.signIN(identifierType,signInDetails.identifier, signInDetails.password)

    ## if any issue is encountered
    if acc == False:
        return {"success":False}
    if passwordHash == acc["items"][5]:
        return {"success": True, "data":{"cart":[], "type":acc["type"], "id":acc["items"][0], "firstName":acc["items"][1], "lastName":acc["items"][2], "phoneNumber":acc["items"][3], "email":acc["items"][4], "address":acc["items"][6]}}
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