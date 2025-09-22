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
    item_ids = cartlist.split(",")
    items = db.get_cart_contents(ids=item_ids)
    return {"success": True, "data": items}

@router.get("/getProductDetails/{ProductID}")
def getProductDetails(ProductID:str):
    item = db.get_product_details(ProductID)
    return {"success": True, "data": item} if item else {"success":False}

@router.get("/searchProduct/{filter}")
def searchProduct(filter: str):
    result = db.searchProduct(filter)
    print(result)
    return {"success": True, "data": result} if result != False else {"success":False}

@router.post("/place_order")
def placeOrder(orderDetails: orderData, verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
    
    result = db.placeOrder(orderDetails.product, orderDetails.address, verification[1]["id"], orderDetails.amountPaid, orderDetails.quantity)
    return {"success": True} if result else {"success":False}

