from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class Consumer(SQLModel, table=True):
    __tablename__:str ="Consumers"
    id: str = Field(primary_key=True, default_factory=uuid.uuid4().__str__)
    firstName: str
    lastName: str
    email: str = Field(unique=True, index=True)
    phoneNumber: str = Field(unique=True, index=True)
    address: str
    password: str

class Seller(SQLModel, table=True):
    __tablename__:str ="Sellers"
    id: str = Field(primary_key=True, default_factory=uuid.uuid4().__str__)
    firstName: str
    lastName: str
    storeName: str
    email: str = Field(unique=True, index=True)
    phoneNumber: str = Field(unique=True, index=True)
    address: str
    storePhoto: str
    password: str
    cardNumber: str ## this is the id card of the seller i.e ghana card or passport id

class Item(SQLModel, table=True):
    __tablename__: str ="Items"
    id: str = Field(primary_key=True, default_factory=uuid.uuid4().__str__)
    itemName: str
    itemDesc: str
    stockQuantity: int
    itemPrice: str
    itemMainCat: str
    itemSubCat: str
    itemImages: str = Field(default_factory=uuid.uuid4().__str__) ## this holds a uuid that will point to a json file containing all the images in base64
    seller: str = Field(index=True, foreign_key="Sellers.id")

class Order(SQLModel, table=True):
    __tablename__: str="Orders"
    id: str = Field(primary_key=True, default_factory=uuid.uuid4().__str__)
    seller: str = Field(index=True, foreign_key="Sellers.id")
    consumer: str = Field(index=True, foreign_key="Consumers.id")
    item: str = Field(index=True, foreign_key="Items.id")
    quatity: int
    address: str
    amount: str
    status: str| None ## None = orderPlaced, dispatched, completed
    datePlaced: datetime = Field(default_factory=datetime.now)
    dateCompleted: datetime | None

class Restock(SQLModel, table=True):
    __tablename__: str = "Restocks"
    id: str = Field(primary_key=True, default_factory=uuid.uuid4().__str__)
    date: datetime = Field(default_factory=datetime.now)
    amount: int
    seller: str = Field(foreign_key="Sellers.id", index=True)
    item: str = Field(foreign_key="Items.id", index=True)