from fastapi import APIRouter, status, Depends
from typing import Any

from utils.database import DBManip
from utils.dependencies import verify_request
from utils.validators import orderData

router = APIRouter(prefix="/consumer", tags=["Consumer"])
db = DBManip()


@router.get("/getTodaysProducts")
def getHomepageProduct():
    items = db.get_today_items()
    return items

@router.get("/category/{mainCat}/{subCat}")
def getCategory(mainCat:str, subCat:str):
    subCategory = subCat.split(",")
    result = db.getCategories(mainCat, subCategory)
    return {"success":True, "data":result} if result else {"success":False}


@router.get("/get_cart_content/{cartlist}")
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

@router.get("/getProductDetails/{ProductID}")
def getProductDetails(ProductID:str):
    item = db.get_product_details(ProductID)
    return {"success": True, "data": item} if item else {"success":False}

@router.get("/searchProduct/{filter}")
def searchProduct(filter: str):
    result = db.searchProduct(filter)
    return {"success": True, "data": result} if result else {"success":False}

@router.post("/complete_order")
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

