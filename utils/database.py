from sqlmodel import create_engine, SQLModel, Session, select
import hashlib
import uuid
import os
from dotenv import load_dotenv
from datetime import datetime

from .table import Item, Seller, Consumer, Order, Restock

load_dotenv()


class DBManip:
    engine = create_engine(str(os.getenv("DATABASE_URL")), echo=False, connect_args={"check_same_thread": False})
    def __init__(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    def insert_user(self, table, firstName, lastName, contact, email, password: str, address, storeName="", photo="", verification_number=""):
        try:
            acc_id = str(uuid.uuid4())
            encoded_password = password.encode('utf8')        
            passwordHash = hashlib.sha256(encoded_password).hexdigest()
            with Session(self.engine) as session:
                if table == "Consumer":
                    consumer = Consumer(id=acc_id, firstName=firstName, lastName=lastName, email=email, phoneNumber=contact, address=address, password=passwordHash)
                    session.add(consumer)
                    session.commit()
                    session.refresh(consumer)
                else:
                    seller = Seller(id=acc_id, firstName=firstName, lastName=lastName, storeName=storeName, email=email, phoneNumber=contact, address=address, storePhoto=photo, password=passwordHash, cardNumber=verification_number)
                    session.add(seller)
                    session.commit()
                    session.refresh(seller)
        except:
            return False
        return acc_id
    
    def insert_product(self,seller_id, product_photos, name, description, price, quantity, mainCat, subCat):
        try:
            item = Item(itemName=name, itemDesc=description, stockQuantity=quantity, itemPrice=price, seller=seller_id, itemSubCat=subCat, itemMainCat=mainCat)
            with Session(self.engine) as session:
                session.add(item)
                session.commit()
                session.refresh(item)
            return item.id
        except Exception as err:
            return False
    
    def get_store_items(self, id:str):
        cols = [Item.id, Item.itemName, Item.itemDesc, Item.stockQuantity, Item.itemPrice, Item.itemImages]
        try:
            statement = select(*cols).where(Item.seller==id)
            with Session(self.engine) as session:
                items = session.exec(statement=statement).all()
                return items
        except Exception as err:
            return False
    
    def get_today_items(self):
        cols = [Item.id, Item.itemName, Item.itemDesc, Item.itemPrice, Seller.storeName, Item.itemImages]
        try:
            statement = select(*cols).join(Seller)
            with Session(self.engine) as session:
                items = session.exec(statement=statement).all()
                return items
        except Exception as err:
            return False
    
    def get_product_details(self, id: str):
        try:
            statement = select(Item.itemName, Item.itemPrice, Item.itemDesc).where(Item.id==id)
            with Session(self.engine) as session:
                item = session.exec(statement=statement).all()
                return item
        except Exception as err:
            return False
    
    def get_cart_contents(self, id: str):
        try:
            statement = select(Item.itemName, Item.itemPrice, Item.itemDesc, Item.itemImages).where(Item.id==id)
            with Session(self.engine) as session:
                items = session.exec(statement=statement).all()
                return items
        except Exception as err:
            return False
    
    def signIN(self, identifier, acc_type):
        try:
            statement = select(Seller if acc_type == "seller" else Consumer).where((Seller.email==identifier or Seller.phoneNumber==identifier) if acc_type == "seller" else (Consumer.email==identifier or Consumer.phoneNumber==identifier))
            with Session(self.engine) as session:
                acc = session.exec(statement=statement).all()
                return acc
        except Exception as err:
            return False
    
    def placeOrder(self, item_id,consumer_id, address,  amount, quantity):
        try:
            select_statement = select(Item.seller).where(Item.id==item_id)
            with Session(self.engine) as session:
                seller_id = session.exec(statement=select_statement).one()
                order = Order(seller=seller_id, consumer=consumer_id, item=item_id, status=None, address=address, amount=amount, quatity=quantity, dateCompleted=None)
                session.add(order)
                session.commit()
                session.refresh(order)
                return order.id
        except Exception as err:
            return False
    
    def getCategories(self, mainCat, subCat):
        cols = [Item.id, Item.itemName, Item.itemPrice, Seller.storeName, Item.itemImages]
        try:
            select_statement = select(*cols).join(Seller).where(Item.itemMainCat==mainCat and Item.itemSubCat in subCat)
            with Session(self.engine) as session:
                items = session.exec(statement=select_statement).all()
                return items
        except Exception as err:
            return False
    
    def searchProduct(self, filter):
        cols = [Item.id, Item.itemName, Item.itemPrice, Seller.storeName, Item.itemImages]
        try:
            statement = select(*cols).join(Seller).where(Item.itemName.like(f"%{filter}%"))
            with Session(self.engine) as session:
                items = session.exec(statement=statement).all()
                return items
            # select_string = f"""SELECT Products.id, Products.product_name, Products.price, Sellers.store_name, Products.photos FROM Products INNER JOIN Sellers ON Products.seller_id=Sellers.id WHERE Products.product_name LIKE "%{filter}%";"""
            # self.cursor.execute(select_string)
            # return self.cursor.fetchall()
        except Exception as err:
            return False
    
    def restock(self, amount: int, id):
        try:
            select_item_statement = select(Item).where(Item.id==id)
            select_seller_statement = select(Item.seller).where(Item.id==id)
            with Session(self.engine) as session:
                ## updating amounts in items table
                item = session.exec(statement=select_item_statement).one()
                item.stockQuantity += amount
                session.add(item)

                ##selecting seller
                seller = session.exec(select_seller_statement).one()

                ##adding to restock table
                restock = Restock(amount=amount, seller=seller, item=id)
                session.add(restock)
                session.commit()

                # refreshing database
                session.refresh(item)
                session.refresh(restock)

                return restock.id
            # restockID = str(uuid.uuid4())
            # update_query = f"""UPDATE Products SET quantity="{amount}" WHERE Product.id="{id}";"""
            # self.cursor.execute(update_query)
            # select_seller = """SELECT seller_id FROM Products;"""
            # self.cursor.execute(select_seller)
            # seller = self.cursor.fetchall()[0]
            # insert_query = f"""INSERT INTO Restock VALUES ("{restockID}","{id}","{seller}" CURRENT_TIMESTAMP )"""
            # self.cursor.execute(insert_query)
            # self.connection.commit()
            # return restockID
        except Exception as err:
            return False
    
    def getStoreOrders(self, seller_id):
        cols = [Order.id, Order.item, Order.address, Order.amount, Order.quatity, Consumer.firstName, Consumer.lastName, Consumer.phoneNumber]
        statement = select(*cols).join(Consumer).where(Order.seller==id)
        try:
            with Session(self.engine) as session:
                orders = session.exec(statement=statement).all()
                return orders
        except:
            return False
    
    def orderCompleted(self, order_id):
        statement = select(Order).where(Order.id==order_id)
        try:
            with Session(self.engine) as session:
                order = session.exec(statement=statement).one()
                order.dateCompleted = datetime.now()
                order.status = "completed"
                session.add(order)
                session.commit()
                session.refresh(order)
            # update_query = f"""UPDATE Orders SET date_received="{action}" WHERE order_id="{id}";"""
            # self.cursor.execute(update_query)
            # self.connection.commit()
        except:
            return False
        
    def dispatchOrder(self, order_id):
        statement = select(Order).where(Order.id==order_id)
        try:
            with Session(self.engine) as session:
                order = session.exec(statement=statement).one()
                order.status = "dispatched"
                session.add(order)
                session.commit()
                session.refresh(order)
        except:
            return False

    def getOrderStatus(self, order_id):
        statement = select(Order).where(Order.id==order_id)
        try:
            with Session(self.engine) as session:
                order = session.exec(statement=statement)
                return order
        except Exception as err:
            return False

