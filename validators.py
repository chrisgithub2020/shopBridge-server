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
    itemSeller: str
    itemImages: list
    itemDescription: str
    itemName: str
    itemPrice: str
    itemQuantity: str
    itemSubCat: str
    itemMainCat: str

class orderData(BaseModel):
    consumer: str
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
    restockNumber: str

class orderActionData(BaseModel):
    id: str
    action:str
