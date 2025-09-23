from fastapi import Depends, status, APIRouter
from typing import Any

from utils.dependencies import verify_request
from utils.validators import ItemData, restockData, orderActionData
from utils.database import DBManip
from utils.save_item_images import save_images

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
    
    outcome = db.insert_product(verification[1]["id"], data.itemImages, data.itemName,data.itemDescription, data.itemPrice, data.itemQuantity, data.itemMainCat, data.itemSubCat)
    if outcome != False:
        image = save_images(data.itemImages, outcome[1])
        return {"success": True, "data":{"id": outcome[0], "name": data.itemName, "quantity": data.itemQuantity, "price":data.itemPrice, "photo":data.itemImages[0]}, "description":data.itemDescription}
    return {"success":False}



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
    
    result = db.deleteItem(id)
    return result

@router.get("/store_orders")
def get_store_orders(verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
        
    if verification[1]["acc_type"] != "seller":
        return status.HTTP_403_FORBIDDEN

    result = db.get_store_orders(verification[1]["id"])
    return {"success": True, "data": result} if result != False else {"success":False}

@router.get("/store_items")
def get_store_items(verification:tuple[bool, Any]=Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
        
    if verification[1]["acc_type"] != "seller":
        return status.HTTP_403_FORBIDDEN

    items = db.get_store_items(verification[1]["id"])
    print(items)
    return {"success": True, "data":items} if items else {"success":False}

# @router.post("/order_actions")
# def orderActions(action: orderActionData):
#     db.orderAction(action.id, action.action)
#     return {"success": True, "data":True}

@router.get("/order_status/{id}")
def orderStatus(order_id: str):
    response = db.get_order_status(order_id=id)
    return {"success": response}