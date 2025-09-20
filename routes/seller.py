from fastapi import Depends, status, APIRouter
from typing import Any

from utils.dependencies import verify_request
from utils.validators import ItemData, restockData
from utils.database import DBManip

db = DBManip()
router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/add_item_to_store")
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
    
    product_id = db.insert_product(data.itemSeller, data.itemImages, data.itemName,data.itemDescription, data.itemPrice, data.itemQuantity, data.itemMainCat, data.itemSubCat)
    return {"success": True, "data":{"id": product_id, "name": data.itemName, "quantity": data.itemQuantity, "price":data.itemPrice, "photo":data.itemImages[0]}, "description":data.itemDescription} if product_id != False else {"success":False}



@router.post("/restock_item")
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


@router.get("/take_down/{id}")
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

@router.get("/store_orders/{id}")
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

@router.get("/store_items/{id}")
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
