from sqlmodel import SQLModel, Field
import uuid


class Consumer(SQLModel, table=True):
    __tablename__:str ="Consumers"
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    address: str
    password: str

class Seller(SQLModel, table=True):
    __tablename__:str ="Sellers"
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    firstName: str
    lastName: str
    storeName: str
    email: str
    phoneNumber: str
    address: str
    storePhoto: str
    password: str
    cardNumber: str ## this is the id card of the seller i.e ghana card or passport id

class Item(SQLModel, table=True):
    __tablename__: str ="Items"
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    itemName: str
    itemDesc: str
    stockQuantity: str
    itemPrice: str
    itemMainCat: str
    itemSubCat: str
    itemImages: str = Field(default=uuid.uuid4) ## this holds a uuid that will point to a json file containing all the images in base64
    seller: uuid.UUID = Field(index=True, foreign_key="Sellers.id")