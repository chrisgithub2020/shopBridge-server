from pydantic import BaseModel

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
    store_photo: str
    type: str

class ItemData(BaseModel):
    itemImages: list[str]
    itemDescription: str
    itemName: str
    itemPrice: str
    itemQuantity: str
    itemSubCat: str
    itemMainCat: str

class orderData(BaseModel):
    product: str
    amountPaid: float
    address: str
    quantity: str


class singInData(BaseModel):
    identifier: str
    password: str
    acc_type: str

class restockData(BaseModel):
    itemID: str
    restockNumber: int

class orderActionData(BaseModel):
    id: str
    action:str

class takeDownData(BaseModel):
    itemId: str
    storeName: str