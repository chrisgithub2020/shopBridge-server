import sqlite3 
import hashlib
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


class DBManip:
    connection = sqlite3.connect(str(os.getenv("DATABASE_URL")), check_same_thread=False)
    cursor = connection.cursor()

    def insert_user(self, table, firstName, lastName, contact, email, password: str, address, storeName="", photo="", id_number=""):
        insert_string = ""
        acc_id = str(uuid.uuid4())
        encoded_password = password.encode('utf8')        
        passwordHash = hashlib.sha256(encoded_password).hexdigest()
        if table == "Consumers":
            insert_string = f"""INSERT INTO {table} VALUES ("{acc_id}", "{firstName.strip()}", "{lastName.strip()}", "{contact.strip()}", "{email}", "{passwordHash}", "{address.strip()}")"""
            print(insert_string)
        elif table == "Sellers":
            insert_string = f"""INSERT INTO {table} VALUES ("{acc_id}", "{storeName.strip()}", "{str(email.strip())}", "{contact.strip()}", "{firstName.strip()}", "{passwordHash}", "{photo}", "{id_number}")"""
            print(insert_string)
            
        self.cursor.execute(insert_string)
        self.connection.commit()
        return acc_id
    
    def insert_product(self,seller_id, product_photos, name, description, price, quantity, mainCat, subCat):
        try:
            product_id = str(uuid.uuid4())
            insert_string = f"""INSERT INTO Products VALUES ("{product_id}","{seller_id}", "{name}", "{description}","{mainCat}", "{subCat}", "{price}", "{quantity}", "{product_photos}")"""
            self.cursor.execute(insert_string)
            self.connection.commit()
        except Exception as err:
            return False

        return product_id
    
    def get_store_items(self, id:str):
        try:
            select_string = f"""SELECT id, photos, product_name, product_description, quantity, price FROM Products WHERE seller_id="{id}";"""
            self.cursor.execute(select_string)
            items = self.cursor.fetchall()
        except Exception as err:
            return False
        return items
    
    def get_today_items(self):
        try:
            select_string = f"""SELECT Products.id, Products.product_name, Products.price, Sellers.store_name,Products.photos FROM Products INNER JOIN Sellers ON Products.seller_id=Sellers.id;"""
            self.cursor.execute(select_string)
            items = self.cursor.fetchall()
        except Exception as err:
            return False
        return items
    
    def get_product_details(self, id):
        try:
            select_string = f"""SELECT Products.photos, Products.product_name, Products.price, Products.product_description FROM Products WHERE Products.id="{id}";"""
            self.cursor.execute(select_string)
            items = self.cursor.fetchall()
            return items
        except Exception as err:
            return False
    
    def get_cart_contents(self, id):
        try:
            select_string = f"""SELECT Products.photos, Products.product_name, Products.id, Products.price FROM Products WHERE Products.id='{id}'"""
            self.cursor.execute(select_string)
            items = self.cursor.fetchall()
            return items
        except Exception as err:
            return False
    
    def signIN(self, identifier_type, identifier, acc_type):
        try:
            select_string = f"""SELECT * FROM {acc_type} WHERE {identifier_type}="{identifier}";"""
            self.cursor.execute(select_string)
            acc = self.cursor.fetchall()
            return acc
        except Exception as err:
            return False
    
    def completeOrder(self, product, address, consumer, amount, quantity):
        try:
            order_id = str(uuid.uuid4())
            select_seller = f"""SELECT seller_id FROM Products WHERE id="{product}";"""
            self.cursor.execute(select_seller)
            seller = self.cursor.fetchone()[0]
            insert_order = f"""INSERT INTO Orders VALUES ("{order_id}","{seller}","{consumer}","{product}",CURRENT_TIMESTAMP, "{None}", "{amount}", "{address}", "{quantity}");"""
            self.cursor.execute(insert_order)
            self.connection.commit()
            return order_id
        except Exception as err:
            return False
    
    def getCategories(self, mainCat, subCat):
        try:
            placeholder = ",".join("?" for _ in subCat)
            select_string = F"""SELECT Products.id, Products.product_name, Products.price,Sellers.store_name, Products.photos FROM Products  INNER JOIN Sellers ON Products.seller_id=Sellers.id WHERE main_category="{mainCat}" AND sub_category IN ({placeholder});"""
            self.cursor.execute(select_string, subCat)
            items = self.cursor.fetchall()
            return items
        except Exception as err:
            return False
    
    def searchProduct(self, filter):
        try:
            select_string = f"""SELECT Products.id, Products.product_name, Products.price, Sellers.store_name, Products.photos FROM Products INNER JOIN Sellers ON Products.seller_id=Sellers.id WHERE Products.product_name LIKE "%{filter}%";"""
            self.cursor.execute(select_string)
            return self.cursor.fetchall()
        except Exception as err:
            return False
    
    def restock(self, amount, id):
        try:
            restockID = str(uuid.uuid4())
            update_query = f"""UPDATE Products SET quantity="{amount}" WHERE Product.id="{id}";"""
            self.cursor.execute(update_query)
            select_seller = """SELECT seller_id FROM Products;"""
            self.cursor.execute(select_seller)
            seller = self.cursor.fetchall()[0]
            insert_query = f"""INSERT INTO Restock VALUES ("{restockID}","{id}","{seller}" CURRENT_TIMESTAMP )"""
            self.cursor.execute(insert_query)
            self.connection.commit()
            return restockID
        except Exception as err:
            return False
    
    def getStoreOrders(self, id):
        try:
            select_query = f"""SELECT Orders.order_id, Consumers.first_name, Consumers.last_name, Orders.product_id, Consumers.contact, Orders.address, Orders.amount_paid, Orders.quantity FROM Orders INNER JOIN Consumers ON Consumers.id=Orders.consumer_id WHERE Orders.seller_id="{id}";"""
            self.cursor.execute(select_query)
            return self.cursor.fetchall()
        except:
            return False
    
    def orderAction(self, id, action):
        try:
            update_query = f"""UPDATE Orders SET date_received="{action}" WHERE order_id="{id}";"""
            self.cursor.execute(update_query)
            self.connection.commit()
        except:
            return False

    def orderStatus(self, id):
        try:
            select_query = f"""SELECT date_received FROM Orders WHERE order_id="{id}";"""
            self.cursor.execute(select_query)
            item = self.cursor.fetchall()[0][0]
            return item
        except Exception as err:
            return False

